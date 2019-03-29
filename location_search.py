"""Functions to geocode urls and save locations and articles to db"""

import googlemaps
import os
import re
import datetime
from collections import namedtuple
from model import connect_to_db, db, User, Location, Attraction
from flask import flash
from distance_matrix import write_distance_matrix_db
from beautiful_soup import (beautiful_soup, search_url_image, search_url_title, 
    search_url_head_title, search_url_author, search_url_site_name, 
    search_url_twitter)

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))
Search = namedtuple('Search',['location', 'match_type'])


def search_url(url, helper_search_terms=''):
    """find a lat and lng for the raw url submission"""

    location = gmaps.geocode(address=f'{helper_search_terms} {url}')

    if len(location) == 1 and not location[0].get('partial_match'):
        return Search(location[0], 'exact')
    else:
        return Search('no location', 'no match type')


def search_cleaned_url(url, helper_search_terms=''):
    """find a lat and lng for the cleaned url submission"""

    cleaned_url = re.sub('[^a-zA-Z0-9]+', ' ', url) #Matches non-alphanumeric

    garbage_text = ['http', 'https', 'www', 'com']

    for garbage in garbage_text:
        if garbage in cleaned_url :
            # Replace the string
            cleaned_url = cleaned_url.replace(garbage, '')

    location = gmaps.geocode(address=f'{helper_search_terms} {cleaned_url}')

    if len(location) == 0:
        return Search(location, 'no match')
    elif len(location) == 1: 
        return Search(location[0], 'exact')
    elif len(location) > 1:
        return Search(location, 'multi_match')
        

def location_for_exact_match(location_result):
    """
    if a single lat and lng can be matched to a url, get additional
    location details.
    """

    place_id = location_result['place_id']
    formatted_address = location_result['formatted_address']
    lat = location_result.get('geometry')['location']['lat']
    lng = location_result.get('geometry')['location']['lng']
    business_name = search_business_name(place_id)

    return (place_id, formatted_address, lat, lng, business_name)


def add_exact_match(location_result, user_id, url, recommended_by=''):
    """
    if a single lat and lng can be matched to a url, save location 
    details to database, save attraction details to database.
    """

    place_id,formatted_address,lat,lng,business_name = location_for_exact_match(location_result)

    existing_location = Location.query.get(place_id)
    existing_location_other_users = Location.query.options(
        db.joinedload('attractions')
        ).filter(
        Location.place_id==place_id, 
        Attraction.user_id != user_id,
        ).first()

    existing_attraction = Attraction.query.filter(
        Attraction.user_id == user_id, 
        Attraction.url==url
        ).first()   

    if not existing_location:
        new_location = Location(
            place_id=place_id, 
            formatted_address=formatted_address, 
            lat=lat, 
            lng=lng,
            business_name=business_name,
            )

        db.session.add(new_location)
        db.session.commit()

    if not existing_attraction:
            dt = datetime.datetime.now().date()
            soup =  beautiful_soup(url)
            
            new_attraction = Attraction(user_id=user_id, 
                place_id=place_id, 
                url=url, 
                recommended_by=recommended_by,
                date_stamp = dt.strftime('%Y-%m-%d'),
                url_img = search_url_image(url,soup),
                url_title = search_url_title(url,soup),
                url_head_title = search_url_head_title(url,soup),
                url_author = search_url_author(url,soup),
                url_site_name = search_url_site_name(url,soup),
                url_twitter = search_url_twitter(url,soup),
                )

            db.session.add(new_attraction)
            db.session.commit()


def search_business_name(place_id):
    """
    Call to places API to get human-readable name for the returned 
    result. This is usually the canonical business name.
    """

    place = gmaps.place(place_id, fields=['name'])
    return place['result']['name']

def delete_attraction(attraction_id):
    """Delete an attraction. Levered in user profile route to manage places."""

    attraction = Attraction.query.get(attraction_id)

    db.session.delete(attraction)
    db.session.commit()

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
