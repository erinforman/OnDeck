import googlemaps
import os
from collections import namedtuple

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))


def search_raw_url_location(url):

    """find a location for the raw url submission"""

    location = gmaps.geocode(address=url)
    Search = namedtuple('Search',['location', 'match_type'])

    if len(location) == 0:

        match_type = 'no_match'
        location_dict = 'no_results'

    elif len(location) == 1:
        #if 1 location was returned for the search
        location_dict = location[0]
        #take the dictionary out of the result list
        if location_dict.get('partial_match'):
        #determine if it was a partial or exact match
            match_type = 'partial'
        else:
            match_type = 'exact'
    else:
        
        location_dict = location
        match_type = 'multi'

    return Search(location_dict, match_type)

#result.location
#x = {'address_components': [{'long_name': "Martha's Vineyard", 'short_name': "Martha's Vineyard", 'types': ['establishment', 'natural_feature']}, {'long_name': 'Dukes County', 'short_name': 'Dukes County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Massachusetts', 'short_name': 'MA', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}], 'formatted_address': "Martha's Vineyard, Massachusetts, USA", 'geometry': {'bounds': {'northeast': {'lat': 41.4830865, 'lng': -70.4666525}, 'southwest': {'lat': 41.3013385, 'lng': -70.8384908}}, 'location': {'lat': 41.3804981, 'lng': -70.645473}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 41.4830865, 'lng': -70.4666525}, 'southwest': {'lat': 41.3013385, 'lng': -70.8384908}}}, 'place_id': 'ChIJOxU0AIkl5YkRQ7y05Pwt1_U', 'types': ['establishment', 'natural_feature']}
def parse_exact_match_results(location_dict):

    #add check on if match type is exact? create a class where function can only act on exacts?
    place_id = location_dict['place_id']
    formatted_address = location_dict['formatted_address']
    lat = location_dict.get('geometry')['location']['lat']
    lng = location_dict.get('geometry')['location']['lng']

    return(place_id, formatted_address, lat, lng)


# def exact_match_location(location):

# raw = search_raw_url_location(url) 

# def main_function(url):
#     if len(raw) == 1 and 

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