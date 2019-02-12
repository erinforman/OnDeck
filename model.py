"""Models and database functions for HB Final Travel Project."""

from flask_sqlalchemy import SQLAlchemy

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

    locations = db.relationship("Location", secondary = "attractions", backref = "users") 

    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email} \
        password={self.password} fname={self.fname} lname={self.lname}>"

class Location(db.Model):
    """Locations assigned to attractions on website."""

    __tablename__ = "locations" #dim

    place_id = db.Column(db.String(64), primary_key=True) #corresponds to place_id in google API
    formatted_address = db.Column(db.String(200), nullable=False)
    street_number = db.Column(db.Integer(10), nullable=False)
    street_name = db.Column(db.String(64), nullable=False) #google route
    city = db.Column(db.String(64), nullable=False) #locality
    state = db.Column(db.String(64), nullable=False) #administrative_area_level_1
    country = db.Column(db.String(64), nullable=False) #country short name
    lat = db.Column(db.Float, nullable=False) #geometry location
    lng = db.Column(db.Float, nullable=False) #geometry location

    def __repr__(self):

        return f"<Location place_id={self.place_id} formatted_address={self.formatted_address} \
        street_number={self.street_number} street_name={self.street_name} city={self.city} \
        state={self.state} country={self.country} lat={self.lat} lng={self.lng}>"


class Attraction(db.Model):
    """Locations assigned to attractions on website."""

    __tablename__ = "attractions" #fact

    attraction_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    #generated when a user adds a link to an attraction to their map
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    place_id = db.Column(db.Integer, db.ForeignKey('locations.place_id'))
    url = db.Column(db.String(200), nullable=False) 
    recommended_by = db.Column(db.String(100), nullable=True) 
    date_stamp = db.Column(db.DateTime, nullable=False) 

    def __repr__(self):

        return f"<Attraction attraction_id={self.attraction_id} user_id={self.user_id} \
        place_id={self.place_id} url={self.url} recommend_by={self.recommend_by} \
        date_stamp={self.date_stamp}>"


##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use maps PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///maps'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    #app.config['SQLALCHEMY_ECHO'] = True

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")