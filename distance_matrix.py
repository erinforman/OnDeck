import googlemaps, os, pprint
from model import connect_to_db, db, User, Location, Attraction, Trip
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))


def write_distance_matrix_db(user_id, units='imperial'):

    #Retrieve all of a users locations.
    user_locations = db.session.query(Location.place_id, Location.lat, Location.lng
                                    ).join(Attraction
                                    ).filter(Attraction.user_id == user_id
                                    ).all()
    
    #Retrieve all of a users locations which do not have a trip i.e. have no route between itself an any other location.
    origins_without_trips = db.session.query(Location.place_id, Location.lat, Location.lng
                                            ).join(Attraction
                                            ).outerjoin(Trip
                                            ).filter(
                                                Attraction.user_id == user_id, 
                                                Trip.origin_place_id == None,
                                            ).all()
    
    #For origin, loop through every location without a trip. For destination, loop through every location. 
    for origin in origins_without_trips:
        
        for destination in user_locations:
  
            if origin.place_id == destination.place_id:
                continue
             
            duration_dict = gmaps.distance_matrix((origin.lat + ',' + origin.lng), (destination.lat + ',' + destination.lng), units=units)
            
            if duration_dict["rows"][0]['elements'][0].get('duration'):
                """Includes trips that can only be road trips. Travel mode is driving."""

                duration_sec = duration_dict["rows"][0]['elements'][0]['duration']['value']
                

                new_trip = Trip(origin_place_id=origin.place_id, 
                                origin_coords=(origin.lat + ',' + origin.lng), 
                                destination_place_id=destination.place_id, 
                                destination_coords=(destination.lat + ',' + destination.lng), 
                                duration=duration_sec)

              
                db.session.add(new_trip)
                db.session.commit()


def mins_to_next_destination(user_id, origin_place_id, excluded_destinations = set()):
    """A trip means to travel between two points: an origin and a destination.
    An itinerary is made up of one or more trips."""

    #Given a user id and origin, find how far away (in mins) the closest destination is
    closest_destination_mins_obj = db.session.query(func.min(Trip.duration) 
                                                        ).join(Location
                                                        ).join(Attraction
                                                        ).filter(
                                                            Attraction.user_id == user_id, 
                                                            Trip.origin_place_id == origin_place_id,
                                                            #Don't return to places we've already been
                                                            (~Trip.destination_place_id.in_(excluded_destinations)),
                                                        ).first()

    #This will be None if the only destination options are excluded destinations or there
    # are no trips because you can't drive from the origin to any other user location 
    # (e.g. Zermatt (car-less city), a single location on Maui)
    closest_destination_mins_int = [row for row in closest_destination_mins_obj][0]

    return closest_destination_mins_int


def create_itinerary(user_id, origin_place_id, duration):

    """
    given a place_id for an origin and a length of time
    in minutes, return an itinerary that takes up the
    given length of time
    """

    itinerary_seq = []
    excluded_destinations = set()
    #no_repeats = set()
    #Keep track of duration requested and time left separately
    time_left = duration
    closest_destination_mins_int = mins_to_next_destination(user_id, origin_place_id, excluded_destinations)

    #If the time it takes to get from an origin to the nearest location exceeds the duration of the itinerary, stop adding to 
    # the itinerary and return it. If the only destination options are no_repeats, stop adding to the intinerary and call it done.

    if closest_destination_mins_int == None:
        #return(itinerary_seq, duration, time_left, duration-time_left)
        return("BLAAAAAAAH")
    
    while closest_destination_mins_int <= time_left:
    #TODO: ADD BETTER HANDLING. IF THE USER SELECTS AN ORIGIN AND A TIME FRAME, WE SHOULD BE ABLE
    #TO PRE-WARN THEM THAT THEY NEED TO WIDEN THEIR TIME FRAME OR ADD MORE LOCATIONS NEARBY
        
        #Given a user id and origin and a duration, find the first trip that matches all criteria.
        trip_obj = db.session.query(Trip,Location
                                    ).join(Location
                                    ).join(Attraction
                                    ).filter(
                                        Attraction.user_id == user_id, 
                                        Trip.origin_place_id == origin_place_id, 
                                        Trip.duration == closest_destination_mins_int,
                                    ).first()
        
        
        if trip_obj:

            #Add origin to no repeats set
            excluded_destinations.add(trip_obj.Trip.origin_place_id)

            #Add trip to itineary                                     
            itinerary_seq.append(trip_obj.Trip.trip_id)

            #Subtract trip duration from time_left
            time_left -= trip_obj.Trip.duration

            #Set trip destination as new trip origin
            origin_place_id = trip_obj.Trip.destination_place_id

            #Calculate time to next nearest location
            closest_destination_mins_int = mins_to_next_destination(user_id, origin_place_id, excluded_destinations)

        if not closest_destination_mins_int:
            
            break



    loc_1 = aliased(Location)
    loc_2 = aliased(Location)
    attr_1 = aliased(Attraction)
    attr_2 = aliased(Attraction)

    trip_details = db.session.query(Trip.trip_id, 
                                    loc_1.business_name.label('business_name_1'),
                                    (attr_1.url.label('url_1')),
                                    loc_2.business_name.label('business_name_2'),
                                    (attr_2.url.label('url_2')),
                                    Trip.duration,
                                    ).join(loc_1, Trip.origin_place_id == loc_1.place_id
                                    ).join(loc_2, Trip.destination_place_id == loc_2.place_id
                                    ).join(attr_1, Trip.origin_place_id == attr_1.place_id
                                    ).join(attr_2, Trip.destination_place_id == attr_2.place_id
                                    ).filter(
                                        attr_1.user_id == user_id, 
                                        attr_2.user_id == user_id, 
                                        (Trip.trip_id.in_(itinerary_seq)),
                                    ).all()

    print(trip_details[0].url_1)
    print(trip_details[0].url_2)
    for trip_id in itinerary_seq:
        for details in trip_details:
            if trip_id == details.trip_id:
                print(f' trip id : {details.trip_id}')
                print(f' origin : {details.business_name_1}')
                print(f' origin_url: {details.url_1}')
                print(f' destination: {details.business_name_2}')
                print(f' destination_url : {details.url_2}')
                print(f' leg duration : {details.duration}')
                print()


    return(itinerary_seq, trip_details, duration, time_left, duration-time_left)







#TODO: the trips in the itinerary need an order enforced.










































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