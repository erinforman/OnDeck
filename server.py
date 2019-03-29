import os
import ast
import sendgrid
from sendgrid.helpers.mail import *
from flask import (Flask, render_template, request, flash, redirect, session, 
    jsonify, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pformat
from sqlalchemy.sql import func

from location_search import (search_url, search_cleaned_url, 
    location_for_exact_match, add_exact_match, search_business_name, 
    delete_attraction)
from distance_matrix import create_itinerary, write_distance_matrix_db
from model import connect_to_db, db, User, Location, Attraction
from urllib.request import urlopen

app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

@app.route('/')
def index():
    """Show homepage and login form."""

    if session:
        session.clear()

    return render_template('homepage.html')
 
@app.route('/login', methods=['POST'])
def check_valid_login():
    """Check if login info is valid"""

    email = request.form['email']
    password = request.form['password']
    user = User.query.filter(User.email == email).first()
    
    if not user:
        session.pop('_flashes', None)
        flash('We do not recognize that e-mail address. New user? Register!')
        return render_template('homepage.html') 
    elif password != user.password:
        session.pop('_flashes', None)
        flash('Incorrect password')
        return render_template('homepage.html') 
    else:
        session['user_id'] = user.user_id
        session['user_email'] = email
        session['fname'] = user.fname
        session['lname'] = user.lname
        return redirect(f'/map/{user.user_id}')

    
@app.route('/map/<int:user_id>')
def submit_new_attraction(user_id):
    """Show main user landing page with submission form and map."""

    user = User.query.options(
        db.joinedload('attractions').joinedload('location')
        ).get(user_id)
    
    return render_template('map.html', user=user, GOOGLE_KEY=GOOGLE_KEY)

@app.route('/map/<int:user_id>', methods=['POST'])
def find_attraction_location(user_id):
    """categorizes match of url to lat and lng as exact or not exact"""

    url = request.form['url']
    helper_search_terms = request.form['helper_search_terms']
    recommended_by = request.form['recommended_by']
    user_id = session['user_id']

    result = search_url(url, helper_search_terms)

    if session.get('result'):
        session.pop('result')

    if result.match_type == 'exact':
        session['result'] = result.location
        add_exact_match(result.location, user_id, url, recommended_by)
        return jsonify(result.location)
    else:
        result = search_cleaned_url(url, helper_search_terms) 

        if result.match_type == 'exact':
            session['result'] = result.location
            add_exact_match(result.location, user_id, url, recommended_by)
            return jsonify(result.location)
        elif result.match_type == 'multi_match' and len(result.location)<3:
            add_exact_match(result.location[0], user_id, url, recommended_by)
            return jsonify(result.location[0])
        else:
            return redirect(f'/map/{str(user_id)}')


@app.route('/calculate_trips')
def calculate_trips():
    """Add new trips for itinerary"""

    user_id = session['user_id']

    return write_distance_matrix_db(user_id)
    
@app.route('/get_map_coords.json')
def create_map():
    """JSON info about map."""

    user_id = session['user_id']
    #find all attractions connected to the user_id.
    user_details = [
        {key: getattr(data,key) for key in data.keys()}
        for data in db.session.query(
            Location.formatted_address,
            Location.business_name,
            Location.lat, 
            Location.lng,
            Attraction.attraction_id,
            Attraction.url,
            Attraction.url_img,
            Attraction.url_title,
            Attraction.url_head_title,
            Attraction.url_author,
            Attraction.url_site_name,
            Attraction.url_twitter,
            Attraction.recommended_by,
            Attraction.date_stamp,
            User.user_id,
            User.fname,
            User.lname
            ).join(Attraction
            ).join(User
            ).filter(User.user_id == user_id
            ).all()
    ]

    return(jsonify(user_details))

@app.route('/user-profile/<int:user_id>')
def show_user_profile(user_id):
    """Get all of a user's saved locations"""

    result = db.session.query(
        Location.formatted_address,
        Location.business_name,
        Attraction.attraction_id,
        Attraction.url,
        Attraction.url_img,
        Attraction.url_title,
        Attraction.url_head_title,
        Attraction.url_author,
        Attraction.url_site_name,
        Attraction.url_twitter,
        Attraction.recommended_by,
        User.user_id,
        User.fname,
        User.lname
        ).join(Attraction
        ).join(User
        ).filter(User.user_id == user_id
        ).order_by(Location.business_name).all()

    return render_template('user_profile.html', result = result, 
        user_id = user_id)

@app.route('/user-profile/<int:user_id>', methods=['POST'])
def delete_attractions(user_id):
    """Remove one or more of a user's locations"""

    attraction_ids = request.form.getlist('check_list')

    if not attraction_ids:
        flash('Select at least one location.', 'error')

    for a_id in attraction_ids:
        delete_attraction(a_id)

    return redirect(f'/user-profile/{str(user_id)}')

@app.route('/itinerary/<int:user_id>')
def select_itinerary_parameters(user_id):
    """Show an itinerary"""

    result = db.session.query(
        Location.place_id,
        Location.formatted_address,
        Location.business_name,
        Attraction.attraction_id,
        Attraction.url,
        Attraction.recommended_by,
        User.user_id,
        User.fname,
        User.lname
        ).join(Attraction
        ).join(User
        ).filter(User.user_id == user_id
        ).order_by(Location.business_name).all()

    return render_template('itinerary.html', result = result, user_id = user_id)

@app.route('/itinerary.json')
def create_itinerary_from_parameters():
    """Create an itinerary from user input of origin and duration"""

    user_id = session['user_id']
    origin_place_id = request.args['origin_place_id']
    hours = request.args['hours']
    days = request.args['days']
    duration = (int(hours) * 3600) + (int(days) * 86400)
    session['hours'] = hours
    session['days'] = days

    itinerary = create_itinerary(user_id, origin_place_id, duration)

    if duration == 0:
        return jsonify(itinerary)
    elif itinerary[0] == 'need_more_time':
        return jsonify(itinerary)
    elif itinerary[0] == 'no_trips':
        return jsonify(itinerary)
    else:
        session.pop('itinerary_details', None)
        session['itinerary_details'] = itinerary.itinerary_details
        return jsonify(itinerary)


@app.route('/itinerary/<int:user_id>', methods=['POST'])
def email_itinerary(user_id):
    """Email an itinerary from itinerary creation page using sendgrid api"""

    itinerary_details = session['itinerary_details']
    fname = session['fname']
    lname = session['lname']
    days = session['days']

    content = f"<p>I planned a trip for us! Pack your bags. We'll be gone for \
        {days} day(s).</p>"
    content += 'Check out the itinerary:<br><br>'

    for i, trip in enumerate(itinerary_details, start=1):

        content += (str(i) + ') <a href="' + trip[3] + '">' + trip[10] + 
            '</a>' + "<br/>")
    
    #Add final destination
    content += (str(len(itinerary_details)+1) + ') <a href="' + 
        itinerary_details[-1][13] + '">' + itinerary_details[-1][20] + '</a>' + 
        "<br/>")
    
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email(session['user_email'])
    to_email = Email(request.form.get('to_email'))
    subject = f'Join {fname} {lname} on a trip!'
    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


    return redirect(f'/itinerary/{str(user_id)}')

# @app.route('/new-user')
# def new_user():
#     pass

#     #TODO: add flow for adding a new user


# @app.route('/new-submission/<int:user_id>')
# def new_submission():
#     """Show form submission page."""
    
#     return render_template('new_submission.html')


if __name__ == '__main__':
    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0")