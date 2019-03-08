import googlemaps, os, pprint
from model import connect_to_db, db, User, Location, Attraction, Trip
from collections import namedtuple
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))

loc_1 = aliased(Location)
loc_2 = aliased(Location)
attrc_1 = aliased(Attraction)
attrc_2 = aliased(Attraction)

def write_distance_matrix_db(user_id, units='imperial'):

    """Retrieve all of a users location pairs for which there is
    not a trip logged"""
  
    trips_leg_a = db.session.query(Location.place_id.label('origin_place_id'), 
        Location.lat.label('origin_lat'),
        Location.lng.label('origin_lng'), 
        Trip.origin_place_id.label('trip_origin_place_id'),
        loc_1.place_id.label('dest_place_id'), 
        loc_1.lat.label('dest_lat'), 
        loc_1.lng.label('dest_lng'), 
        ).join(Attraction
        ).outerjoin(Trip
        ).join(loc_1, loc_1.place_id != Location.place_id
        ).join(attrc_2, attrc_2.place_id == loc_1.place_id
        ).filter(Attraction.user_id == user_id, attrc_2.user_id == user_id, 
        Trip.origin_place_id.is_(None)
        ).distinct()

    trips_leg_b_sub = trips_leg_a.subquery()

    trips_leg_b = db.session.query(trips_leg_b_sub.c.dest_place_id.label('origin_place_id'), 
        trips_leg_b_sub.c.dest_lat.label('origin_lat'),
        trips_leg_b_sub.c.dest_lng.label('origin_lng'),
        trips_leg_b_sub.c.trip_origin_place_id.label('trip_origin_place_id'),
        trips_leg_b_sub.c.origin_place_id.label('dest_place_id'),
        trips_leg_b_sub.c.origin_lat.label('dest_lat'),
        trips_leg_b_sub.c.origin_lng.label('dest_lng'),).distinct()

    trips = trips_leg_b.union(trips_leg_a).all()

    #TODO: check if new trips get added when new origins are added (ie another row for coit and santa cruz when santa cruz is added)
    new_trips = []

    for trip in trips:

        duration_dict = gmaps.distance_matrix((trip.origin_lat + ',' + trip.origin_lng), 
            (trip.dest_lat + ',' + trip.dest_lng), units = units)
         
        if duration_dict["rows"][0]['elements'][0].get('duration'):
            """Includes trips that can only be road trips. Travel mode is driving. 
            Duration unit is seconds."""
            duration_sec = duration_dict["rows"][0]['elements'][0]['duration']['value']

            new_trips.append(Trip(origin_place_id = trip.origin_place_id, 
                            origin_coords = (trip.origin_lat + ',' + trip.origin_lng), 
                            destination_place_id = trip.dest_place_id, 
                            destination_coords = (trip.dest_lat + ',' + trip.dest_lng), 
                            duration = duration_sec))

    if new_trips:

        db.session.add_all(new_trips)          
        db.session.commit()


def get_next_trip(user_id, origin_place_id, excluded_destinations):

    """A trip means to travel between two points: an origin and a destination.
    An itinerary is made up of one or more trips."""

    #Given a user id and origin, find how far away (in seconds) the closest destination is

    try:
        next_trip =  db.session.query(
            Trip.trip_id,
            Trip.duration,
            Trip.origin_place_id,
            attrc_1.url.label('url_1'),
            loc_1.business_name.label('business_name_1'),
            Trip.destination_place_id,
            attrc_2.url.label('url_2'), 
            loc_2.business_name.label('business_name_2'),
            ).join(attrc_1, attrc_1.place_id == Trip.origin_place_id
            ).join(attrc_2, attrc_2.place_id == Trip.destination_place_id
            ).join(loc_1, loc_1.place_id == Trip.origin_place_id
            ).join(loc_2, loc_2.place_id == Trip.destination_place_id 
            ).filter(
                attrc_1.user_id == user_id, 
                attrc_2.user_id == user_id,  
                Trip.origin_place_id == origin_place_id,
                #Don't return to places we've already been
                (~Trip.destination_place_id.in_(excluded_destinations)),
            ).order_by(Trip.duration).first()
    except:

        return 

    else:
        return next_trip




    #This will be None if the only destination options are excluded destinations or there
    # are no trips because you can't drive from the origin to any other user location 
    # (e.g. Zermatt (car-less city), a single location on Maui)
    #cmd+d highlights all the things you want.
   

def create_itinerary(user_id, origin_place_id, duration):

    """
    given a place_id for an origin and a length of time
    in seconds, return an itinerary that takes up the
    given length of time
    """
    Itinerary = namedtuple('Itinerary',['itinerary_seq', 'itinerary_details', 
        'duration', 'time_left', 'time_spent'])
 
    itinerary_seq = []
    itinerary_details = []
    excluded_destinations = set()
    #no_repeats = set()
    #Keep track of duration requested and time left separately
    time_left = duration
    next_trip = get_next_trip(user_id, origin_place_id, excluded_destinations)


    #If the time it takes to get from an origin to the nearest location exceeds the duration of the itinerary, stop adding to 
    # the itinerary and return it. If the only destination options are no_repeats, stop adding to the intinerary and call it done.

    if next_trip == None:
        #return(itinerary_seq, duration, time_left, duration-time_left)
        return('no_trips', next_trip)
        # BLAAAAAAAH ****** No man is an island...or a car-less city")

    if next_trip.duration > time_left:
        # return((f'BLAAAAAAAH ***** itinerary of one: {origin_place_id}'))
        return('need_more_time',next_trip,duration)

    while next_trip.duration <= time_left:

    #TODO: ADD BETTER HANDLING. IF THE USER SELECTS AN ORIGIN AND A TIME FRAME, WE SHOULD BE ABLE
    #TO PRE-WARN THEM THAT THEY NEED TO WIDEN THEIR TIME FRAME OR ADD MORE LOCATIONS NEARBY

        #Add origin to no repeats set
        excluded_destinations.add(next_trip.origin_place_id)

        #Add trip to itineary                                     
        itinerary_seq.append(next_trip.trip_id)
        itinerary_details.append(next_trip)

        #Subtract trip duration from time_left
        time_left -= next_trip.duration

        #Set trip destination as new trip origin
        origin_place_id = next_trip.destination_place_id

        #Calculate time to next nearest location
        next_trip = get_next_trip(user_id, origin_place_id, excluded_destinations)

        if not next_trip:
            
            break

        # for trip_id in itinerary_seq:

        #     for details in trip_details:
        #         if trip_id == details.trip_id:
        #             print(f' trip id : {details.trip_id}')
        #             print(f' origin : {details.business_name_1}')
        #             print(f' origin_url: {details.url_1}')
        #             print(f' destination: {details.business_name_2}')
        #             print(f' destination_url : {details.url_2}')
        #             print(f' leg duration : {details.duration}')
        #             print()

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(itinerary_details)

    return Itinerary(itinerary_seq, itinerary_details, duration, time_left, duration-time_left)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)