import googlemaps, os, pprint
from model import connect_to_db, db, User, Location, Attraction, Trip

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))


def write_distance_matrix_db(user_id,units='imperial',origins=None,destinations=None):



    #first retrieve all of a users locations
    user_locations = db.session.query(Location.place_id, Location.lat, Location.lng).join(Attraction).join(Trip).filter(Attraction.user_id == user_id).all()
    #don't calculate pairs for locations that don't exist together in a users attractions
    #TODO add check to see if location is already in trips table.
    for origin in user_locations:
        for destination in user_locations:
            if origin.place_id == destination.place_id:
                continue

            duration_dict = gmaps.distance_matrix((origin.lat + ',' + origin.lng), (destination.lat + ',' + destination.lng), units=units)
            
            #add logic to check if the pair already exists in the table. if it does,
            # don't add it.


            if duration_dict["rows"][0]['elements'][0].get('duration'):
                """trips that can only be road trips. travel mode is driving."""

                duration_sec = duration_dict["rows"][0]['elements'][0]['duration']['value']

                new_trip = Trip(origin_place_id=origin.place_id, 
                                origin_coords=(origin.lat + ',' + origin.lng), 
                                destination_place_id=destination.place_id, 
                                destination_coords=(destination.lat + ',' + destination.lng), 
                                duration=duration_sec)


                db.session.add(new_trip)
                db.session.commit()




CITIES_LATLONG = {
    'Forestville': {'lat': 38.473625, 'lon': -122.889992},
    'Houston': {'lat': 29.749907, 'lon': -95.358421},
    'Tempe': {'lat': 33.427204, 'lon': -111.939896},
}


def get_distance_matrix(units="imperial"):
    """given an origin latlong and dest latlong, return the distance
    matrix json"""
    city_latlongs = []
    for k,v in iter(CITIES_LATLONG.items()):
        print("item: ", k,v)
        city_latlongs.append(tuple(v.values()))
    print("citylatlongs: %s" % city_latlongs)

    out = gmaps.distance_matrix(
        city_latlongs, city_latlongs, units=units
    )
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(out)
    return out


def print_matrix(dm):
    """given a distance matrix dict, pretty print the output."""
    origin_idx = 0
    dest_idx = 0
    rows = dm['rows']
    for origin_addr in dm['origin_addresses']:
        print("Origin Address: %s" % origin_addr)
        for destination_addr in dm['destination_addresses']:
            print("Destination Address: %s" % destination_addr)
            distances = rows[origin_idx]['elements'][dest_idx]
            print("Distance: %s" % distances['distance']['text'])
            dest_idx = dest_idx + 1
        dest_idx=0
        origin_idx = origin_idx + 1
        print("\n")


if __name__ == "__main__":

    from server import app
    connect_to_db(app)