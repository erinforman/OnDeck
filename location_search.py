import googlemaps
import os

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))


def search_raw_url_location(url):

    """find a location for the raw url submission"""

    location = gmaps.geocode(address=url)

    if len(location) == 0:

        match_type = 'no_match'
        location_dict = None

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

    return [location_dict, match_type]

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