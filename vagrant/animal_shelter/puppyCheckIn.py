from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy, Profile, Adopter
# from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# ### End of boilerplate ###

def checkPuppyIntoShelter(shelter, puppy):


def checkPuppyIn(puppy):
    print puppy.name

all_puppies = session.query(Puppy).all()
for puppy in all_puppies:
    checkPuppyIn(puppy)
