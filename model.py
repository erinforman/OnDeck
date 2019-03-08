"""Models and database functions for HB Final Travel Project."""
#import sys, datetime
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import func


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of travel app."""

    __tablename__ = "users" #dim

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=False)

    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email} \
        password={self.password} fname={self.fname} lname={self.lname}>"

    def __init__(self, email, password, fname, lname):
        
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname

        print("A User object has been created.")

class Location(db.Model):
    """Locations assigned to attractions on website."""

    __tablename__ = "locations" #dim

    place_id = db.Column(db.String(64), primary_key=True) #corresponds to place_id in google API
    formatted_address = db.Column(db.String(200), nullable=False)
    business_name = db.Column(db.String(200), nullable=True)
    lat = db.Column(db.String, nullable=False) #geometry location
    lng = db.Column(db.String, nullable=False) #geometry location

    trips = db.relationship("Trip", backref=db.backref("location"))

    def __repr__(self):

        return f"<Location place_id={self.place_id} formatted_address={self.formatted_address} \
                lat={self.lat} lng={self.lng}>"


class Attraction(db.Model):
    """Locations assigned to attractions on website."""

    __tablename__ = "attractions" #fact

    attraction_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    #generated when a user adds a link to an attraction to their map
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    place_id = db.Column(db.String(64), db.ForeignKey('locations.place_id'))
    url = db.Column(db.String(200), nullable=False) 
    recommended_by = db.Column(db.String(100), nullable=True) 
    date_stamp = db.Column(db.String(64))


    user = db.relationship("User", backref=db.backref("attractions", order_by=attraction_id))
    location = db.relationship("Location", backref=db.backref("attractions", order_by=attraction_id)) 


    def __repr__(self):

        return f"<Attraction attraction_id={self.attraction_id} user_id={self.user_id} \
        place_id={self.place_id} url={self.url} recommended_by={self.recommended_by} \
        date_stamp={self.date_stamp}>"


    def example_data_attraction():
        """Create example data for the test database."""
        # FIXME: write a function that creates a game and adds it to the database.
        # attraction = Game(name="Power Grid",
        #             description="supply the most cities with power")
        # db.session.add(game)
        # db.session.commit()
        # print("FIXME")

        pass


class Trip(db.Model):
    """Distances between Locations assigned to attractions on website."""

    __tablename__ = "trips" #dim

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    origin_place_id = db.Column(db.String(64), db.ForeignKey('locations.place_id'))
    origin_coords = db.Column(db.String(64))
    destination_place_id = db.Column(db.String(64)) #, db.ForeignKey('locations.place_id'))
    destination_coords = db.Column(db.String(64))
    duration = db.Column(db.Integer)




    def __repr__(self):

        return f"<Trip trip_id={self.trip_id} origin_place_id={self.origin_place_id} \
                 origin_coords={self.origin_coords} destination_place_id={self.destination_place_id} \
                 destination_coords={self.destination_coords} duration={self.duration}>"

##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///maps'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    #app.config['SQLALCHEMY_ECHO'] = True

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")