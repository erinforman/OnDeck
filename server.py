import os
import requests
import ast
from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pformat
from sqlalchemy.sql import func

from location_search import search_url, search_cleaned_url, location_for_exact_match, add_exact_match, search_business_name, delete_attraction
from distance_matrix import create_itinerary
from model import connect_to_db, db, User, Location, Attraction


app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

@app.route('/')
def index():
    """Show homepage and login form."""

    #TODO: handle scenario where user is already logged in and lands on homepage

    return render_template('homepage.html', GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)
 
@app.route('/login', methods=['POST'])
def check_valid_login():
    """Check if login info is valid"""
    email = request.form['email']
    password=request.form['password']
    user=User.query.filter(User.email == email).first()
    
    """email address not found in db"""
    if not user:
        flash('We do not recognize that e-mail address. New user? Register!')
        return redirect('/')
        #TODO: HANDLE NEW USER REGISTRATION
    
    """email address found in db but pw doesn't match"""     
    if password != user.password:
        flash('Incorrect password')
        return redirect('/')

    """valid login"""
    session['user_id'] = user.user_id
    flash('Logged in')
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

    url = request.form['url']
    helper_search_terms = request.form['helper_search_terms']
    recommended_by = request.form['recommended_by']
    user_id = session['user_id']

    result = search_url(url, helper_search_terms)

    if result.match_type == 'exact':
        add_exact_match(result.location, user_id, url, recommended_by)
        return redirect(f'/map/{str(user_id)}')
    else:
        result = search_cleaned_url(url, helper_search_terms) 

        if result.match_type == 'exact':
            add_exact_match(result.location, user_id, url, recommended_by)
            return redirect(f'/map/{str(user_id)}')
        elif result.match_type == 'multi_match':
            return redirect(url_for('choose_correct_location', 
                user_id=user_id, 
                url=url,
                recommended_by=recommended_by,
                result=result, 
                ))
        else:
            flash('No results. Try adding details like city or attraction name to help the search out.')
            return redirect(f'/map/{str(user_id)}')


@app.route('/map/<int:user_id>/search-results')
def choose_correct_location(user_id):

    result = ast.literal_eval(request.args.get('result'))

    for location in result:
        location['business_name'] = search_business_name(location['place_id'])
        #business name comes from a different API: Google Places

    url = request.args.get('url')
    recommended_by = request.args.get('recommended_by')

    return render_template('search_results.html', result=result, user_id=user_id, url=url, recommended_by=recommended_by)


@app.route('/map/<int:user_id>/search-results', methods=['POST'])
def add_correct_location(user_id):
    
    url= request.form['url']
    recommended_by = request.form['recommended_by']
    location = ast.literal_eval(request.form.get('location'))

    add_exact_match(location, user_id, url, recommended_by)

    return redirect(f'/map/{str(user_id)}')

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

    return jsonify(user_details)

@app.route('/user-profile/<int:user_id>')
def show_user_profile(user_id):

    result = db.session.query(
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
        ).all()

    return render_template('user_profile.html', result = result, user_id = user_id)

@app.route('/user-profile/<int:user_id>', methods=['POST'])
def delete_attractions(user_id):

    attraction_ids = request.form.getlist('check_list')

    for a_id in attraction_ids:
        delete_attraction(a_id)

    return redirect(f'/user-profile/{str(user_id)}')

@app.route('/itinerary/<int:user_id>')
def select_itinerary_parameters(user_id):

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
        ).all()

    return render_template('itinerary.html', result = result, user_id = user_id)

@app.route('/itinerary.json')
def create_itinerary_from_parameters():
    print(request.args)
    user_id = session['user_id']
    origin_place_id = request.args['origin_place_id']
    print(origin_place_id)
    hours = request.args['hours']
    #print(hours)
    days = request.args['days']
    #print(days)

    duration = (int(hours) * 3600) + (int(days) * 86400)
    print(duration)


    #print(origin_place_id, hours, days, duration)

    itinerary = create_itinerary(user_id, origin_place_id, duration)

    return jsonify(itinerary)

# @app.route('/new-user')
# def new_user():
#     pass

#     #TODO: add flow for adding a new user


# @app.route('/new-submission/<int:user_id>')
# def new_submission():
#     """Show form submission page."""
    
#     return render_template('new_submission.html')


if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")