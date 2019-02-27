import googlemaps, os, pprint
from model import connect_to_db, db, User, Location, Attraction, Trip
from sqlalchemy.sql import func

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


def create_itinerary(origin_place_id,duration):

    """
    given a place_id for an origin and a length of time
    in minutes, return an itinerary that takes up the
    given length of time

    origina_place_id = 'ChIJAQAAQIyAhYARRN3yIQG4hd4'
    time_consumed = 0


    select the origin from the trips table

    select min(duration) from trips where origin_place_id = ';
    select destination_place_id from trips where duration = MIN DURATION ABOVE;

    

    while time_consumed < duration:

    """
    itinerary = []
    no_repeats = set()
    closest_destination_mins_int = 0
    time_left = duration


    #If the closest destination would make the itinerary go over the given iterinary duration, stop adding to the intinerary and call it done.
    while closest_destination_mins_int < time_left:
        #print(f'origin_place_id:  {origin_place_id}, no_repeats:  {no_repeats}')

        #Given a user id and origin, find how far away (in mins) the closest destination is
        closest_destination_mins_obj = db.session.query(func.min(Trip.duration) 
                                                        ).join(Location
                                                        ).join(Attraction
                                                        ).filter(
                                                            Attraction.user_id == user_id, 
                                                            Trip.origin_place_id == origin_place_id,
                                                            #Don't return to places we've already been
                                                            (~Trip.destination_place_id.in_(no_repeats)),
                                                        ).first()
        
        #This will be None if the only destination options are no_repeats.                                             
        closest_destination_mins_int = [row for row in closest_destination_mins_obj][0]

        if closest_destination_mins_int:

            #print(f'closest_destination_mins_int: {closest_destination_mins_int}')

            #Given a user id and origin and a duration, find the first trip that matches all criteria.
            trip_obj = db.session.query(Trip,Location
                                        ).join(Location
                                        ).join(Attraction
                                        ).filter(
                                            Attraction.user_id == user_id, 
                                            Trip.origin_place_id == origin_place_id, 
                                            Trip.duration == closest_destination_mins_int,
                                        ).first()
            #Add trip to itineary
            #print(trip_obj.Trip.trip_id, trip_obj.Location.business_name, itinerary, duration, time_left)
                                     
            itinerary.append(trip_obj.Trip.trip_id)
            #Add origin to no repeats list
            no_repeats.add(trip_obj.Trip.origin_place_id)
            #Subtract time from duration
            time_left -= trip_obj.Trip.duration
            #Set trip destination as new trip origin
            origin_place_id = trip_obj.Trip.destination_place_id
        else:
            #If the only destination options are no_repeats, stop adding to the intinerary and call it done.
            break


    pretty_itenerary = db.session.query(Location.business_name, Attraction.url, User.fname
                                                        ).join(Attraction
                                                        ).join(User
                                                        ).join(Trip
                                                        ).filter(
                                                            Attraction.user_id == user_id, 
                                                            (Trip.trip_id.in_(itinerary)),
                                                        ).all()

    print(pretty_itenerary)

    return (f'Your itinerary!:  {itinerary} Itinerary duration: {duration - time_left} Time left over: {time_left}  Length of vacation: {duration} ')


















































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