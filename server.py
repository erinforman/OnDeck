import os
import requests
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pformat

from location_search import search_raw_url_location, parse_exact_match_results
from model import connect_to_db, db, User, Location, Attraction


app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')

# GOOGLE_URL_1 = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_KEY+"&callback=initMap"
# GOOGLE_URL_2 = "https://maps.googleapis.com/maps/api/js?key="+GOOGLE_KEY+"&libraries=places&callback=initMap" 
# GOOGLE_URL_3 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/output?key="+GOOGLE_KEY+"&input=coit tower&inputtype=textquery"
# GOOGLE_URL_4 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key="+GOOGLE_KEY
# GOOGLE_URL_5 = <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key="+GOOGLE_KEY+"&libraries=places"></script>
# #<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>

@app.route('/')
def submit_login():
    """Show homepage and login form."""

    return render_template('homepage.html')

@app.route('/', methods=['POST'])
def check_valid_login():
    """Check if login info is valid"""

    email=request.form["email"]
    password=request.form["password"]
    user=User.query.filter(User.email==email).first()

    
    if not user:
        """email address not found in db"""
        flash("We don't recognize that e-mail address. New user? Register!")
        return redirect('/')
        #TODO: HANDLE NEW USER REGISTRATION
        
    elif password != user.password:
        """email address found in db but pw doesn't match""" 
        flash('Incorrect password')
        return redirect('/')

    else:
        """valid login"""
        session["user_id"] = user.user_id
        flash("Logged in")
        return redirect(f"/my-map/{user.user_id}")

    
@app.route('/my-map/<int:user_id>')
def submit_new_attraction(user_id):
    """Show main user landing page with submission form and map."""
    user = User.query.options(db.joinedload('attractions').joinedload('location')).get(user_id)
    
    return render_template('my_map.html', user=user)

@app.route('/my-map/<int:user_id>', methods=['POST'])
def find_attraction_location(user_id):

    url = request.form["url"]
    recommended_by = request.form["recommended_by"]
    user_id = session["user_id"]

    result = search_raw_url_location(url)

    if result.match_type == 'exact':

        place_id, formatted_address, lat, lng = parse_exact_match_results(result.location)

        existing_location = Location.query.get(place_id)
        existing_location_other_users = Location.query.options(db.joinedload('attractions')).filter(Location.place_id==place_id, Attraction.user_id != user_id).first()
        existing_attraction = Attraction.query.filter(Attraction.user_id == user_id, Attraction.url==url).first()   


        if not existing_location:

            new_location = Location(place_id=place_id, \
                                    formatted_address=formatted_address, lat=lat, lng=lng)

            db.session.add(new_location)
            db.session.commit()

        if existing_location_other_users:

            flash('Someone else added fun stuff at '+formatted_address+' Check it out <here>.')

        if not existing_attraction:

            new_attraction = Attraction(user_id=user_id, \
                                        place_id=place_id, url=url, recommended_by=recommended_by)

            db.session.add(new_attraction)
            db.session.commit()

            flash('Exact location match! '+formatted_address+' added to map.')

        else:

            flash(formatted_address+' is already on your map.')


        return redirect(f'/my-map/'+str(user_id))

    
    # print('locationnnnnnnnnn----',result.location)
    # print('maaaaatchtype-----',result.match_type)

    return render_template('location_search_results.html', result=result)

@app.route('/bigmapTEST')
def view_map():
    return render_template("big_map.html", GOOGLE_KEY=GOOGLE_KEY)

# @app.route('/new-user')
# def new_user():
#     pass

#     #TODO: add flow for adding a new user


# @app.route('/new-submission/<int:user_id>')
# def new_submission():
#     """Show form submission page."""
    
#     return render_template('new_submission.html')


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")