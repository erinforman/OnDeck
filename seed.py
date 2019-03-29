
from sqlalchemy_utils import database_exists, create_database, drop_database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from model import User, connect_to_db, db

def create_db():

    db_name = 'maps'

    if database_exists('postgresql:///'+db_name):
        drop_database('postgresql:///'+db_name)

    create_database('postgresql:///'+db_name)
 
def create_users():

    ross = User(fname='Ross', lname='Geller', email='ross@test.com', password=1)

    joey = User(fname='Joey', lname='Tribbiani', email='joey@test.com', password=2)

    monica = User(fname='Monica', lname='Geller', email='monica@test.com', password='m')

    db.session.add_all([ross, joey, monica])
    db.session.commit()
    print('Added Users.')


if __name__ == "__main__":
    
    from server import app
    create_db()
    connect_to_db(app)
    db.create_all()
    print('Connected to DB.')
    create_users()
