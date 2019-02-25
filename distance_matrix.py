import googlemaps, os, pprint
from model import connect_to_db, db, User, Location, Attraction, Trip

gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))


def write_distance_matrix_db(user_id, units='imperial'):

    #Retrieve all of a users locations.
    user_locations = db.session.query(Location.place_id, Location.lat, Location.lng).join(Attraction).filter(Attraction.user_id == user_id).all()
    
    #Retrieve all of a users locations which do not have a trip i.e. have no route between itself an any other location.
    origins_without_trips = db.session.query(Location.place_id, Location.lat, Location.lng).join(Attraction).outerjoin(Trip).filter(Attraction.user_id == user_id, Trip.origin_place_id == None).all()
    
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





if __name__ == "__main__":

    from server import app
    connect_to_db(app)