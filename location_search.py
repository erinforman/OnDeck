import googlemaps, os, re, datetime, pytz
from collections import namedtuple
from urllib.parse import urlparse
from model import db, User, Location, Attraction, Trip
from flask import flash

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))
pacific = pytz.timezone('US/Pacific')


def search_url(url, helper_search_terms):

    """find a location for the raw url submission"""

    if helper_search_terms:

        location = gmaps.geocode(address=helper_search_terms+' '+url)

    else:

        location = gmaps.geocode(address=url)

    Search = namedtuple('Search',['location', 'match_type'])

    if len(location) == 1 and not location[0].get('partial_match'):

        return Search(location[0], 'exact')

    else:

        return Search('no location', 'no match type')

def search_cleaned_url(url, helper_search_terms):

    """find a location for the cleaned url submission"""

    cleaned_url = re.sub('[^a-zA-Z0-9]+', ' ', url) #Matches non-alphanumeric

    garbage_text = ['http', 'https', 'www', 'com']

    for garbage in garbage_text:

        if garbage in cleaned_url :
            # Replace the string
            cleaned_url = cleaned_url.replace(garbage, '')
    
    """
    alt method of cleaning url
    pattern = re.compile('\w+')
    ' '.join(pattern.findall(url))
    """
    if helper_search_terms:

        location = gmaps.geocode(address=helper_search_terms+' '+cleaned_url)

    else:

        location = gmaps.geocode(address=cleaned_url)

    Search = namedtuple('Search',['location', 'match_type'])

    if len(location) == 0:

        return Search(location, 'no match')

    elif len(location) == 1: 

        #includes location[0].get('partial_match'):

        return Search(location[0], 'exact')

    elif len(location) > 1:

        return Search(location, 'multi_match')
        


def location_for_exact_match(location_result):

    place_id = location_result['place_id']
    formatted_address = location_result['formatted_address']
    lat = location_result.get('geometry')['location']['lat']
    lng = location_result.get('geometry')['location']['lng']
    business_name = search_business_name(place_id)

    return(place_id, formatted_address, lat, lng, business_name)


def add_exact_match(location_result, user_id, url, recommended_by=''):

    place_id, formatted_address, lat, lng, business_name = location_for_exact_match(location_result)

    existing_location = Location.query.get(place_id)
    existing_location_other_users = Location.query.options(db.joinedload('attractions')).filter(Location.place_id==place_id, Attraction.user_id != user_id).first()
    existing_attraction = Attraction.query.filter(Attraction.user_id == user_id, Attraction.url==url).first()   

    if not existing_location:

            new_location = Location(
                place_id=place_id, 
                formatted_address=formatted_address, 
                lat=lat, 
                lng=lng,
                business_name=business_name
            )

            db.session.add(new_location)
            db.session.commit()

    if existing_location_other_users:

        flash('Someone else added fun stuff at '+formatted_address+' Check it out <here>.')

    if not existing_attraction:

            dt = datetime.datetime.now().date()
            
           

            new_attraction = Attraction(user_id=user_id, 
                                        place_id=place_id, 
                                        url=url, 
                                        recommended_by=recommended_by,
                                        date_stamp = dt.strftime("%Y-%m-%d")
                                   
                                        )

            db.session.add(new_attraction)
            db.session.commit()

            flash('Exact location match! '+business_name+' at '+formatted_address+' added to map.')

    else:

        flash(business_name+' is already on your map.')


def search_business_name(place_id):

    """Call to places API to retrieve human-readable name for the returned result. 
    This is usually the canonicalized business name."""

    return gmaps.place(place_id,fields=['name'])['result']['name']

def delete_attraction(attraction_id):

    attraction = Attraction.query.get(attraction_id)

    db.session.delete(attraction)
    db.session.commit()

# main_function(url)    
"""
gmaps.geocode(address='pizza')
gmaps.geocode(address='pariscemeteries calvaire')
z=gmaps.geocode(address='cnn') #1 exact result
z=gmaps.geocode(address='www.cnn.com') #2 exact results
len(z)
z=gmaps.geocode(address='disney')
 x=gmaps.places_autocomplete_query('pizza in new york')
 x=gmaps.find_place('pizza in new york', 'textquery')
 x=gmaps.find_place('pizza in new york', 'textquery')
x=gmaps.find_place('pizza in new york', 'textquery', fields=['icon', 'price_level', 'photos', 'name', 'geometry', 'place_id', 'permanently_closed', 'rating', 'id', 'types', 'opening_hours', 'plus_code', 'formatted_address'])
for key, value in x.items():
...     print(key,':::', value)

y = x.get('candidates')
for a in y:
...     print(a)

response = requests.get(url)

x=gmaps.find_place('paris cemeteries calvaire', 'textquery',fields=['icon', 'price_level', 'photos', 'name', 'geometry', 'place_id', 'permanently_closed', 'rating', 'id', 'types', 'opening_hours', 'plus_code', 'formatted_address'])

>>> x=gmaps.find_place('pariscemeteriescalvaire', 'textquery',fields=['icon', 'price_level', 'photos', 'name', 'geometry', 'place_id', 'permanently_closed', 'rating', 'id', 'types', 'opening_hours', 'plus_code', 'formatted_address'])
>>> x
{'candidates': [], 'status': 'ZERO_RESULTS'}
>>> x=gmaps.find_place('paris cemeteries calvaire', 'textquery',fields=['icon', 'price_level', 'photos', 'name', 'geometry', 'place_id', 'permanently_closed', 'rating', 'id', 'types', 'opening_hours', 'plus_code', 'formatted_address'])
>>> x
{'candidates': [{'formatted_address': '2 Rue du Mont-Cenis, 75018 Paris, France', 'geometry': {'location': {'lat': 48.8868433, 'lng'

 y=gmaps.places_autocomplete('paris', session_token = '1')


response = requests.get(GOOGLE_URL_4)
data = response.json()
print(data)
for key,value in data.items():
...     print(key,value)
data.get("status")
data.get("candidates")
"""