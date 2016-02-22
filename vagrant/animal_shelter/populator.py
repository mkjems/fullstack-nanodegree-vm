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


# #### Delete #####

session.query(Shelter).delete()
session.commit()
session.query(Profile).delete()
session.commit()
session.query(Puppy).delete()
session.commit()


# Add Shelters
shelter1 = Shelter(
    name="Oakland Animal Services",
    address="1101 29th Ave",
    city="Oakland",
    state="California",
    zipCode="94601",
    website="oaklandanimalservices.org",
    maximum_capacity=25,
    current_occupancy=0)
session.add(shelter1)

shelter2 = Shelter(
    name="San Francisco SPCA Mission Adoption Center",
    address="250 Florida St",
    city="San Francisco",
    state="California",
    zipCode="94103",
    website="sfspca.org",
    maximum_capacity=25,
    current_occupancy=0,
)
session.add(shelter2)

shelter3 = Shelter(
    name="Wonder Dog Rescue",
    address="2926 16th Street",
    city="San Francisco",
    state="California",
    zipCode="94103",
    website="http://wonderdogrescue.org",
    maximum_capacity=25,
    current_occupancy=0)
session.add(shelter3)

shelter4 = Shelter(
    name="Humane Society of Alameda",
    address="PO Box 1571",
    city="Alameda",
    state="California",
    zipCode="94501",
    website="hsalameda.org",
    maximum_capacity=25,
    current_occupancy=0)
session.add(shelter4)

shelter5 = Shelter(
    name="Palo Alto Humane Society",
    address="1149 Chestnut St.",
    city="Menlo Park",
    state="California",
    zipCode="94025",
    website="paloaltohumane.org",
    maximum_capacity=25,
    current_occupancy=0
)
session.add(shelter5)


# Add Puppies

male_names = [
    "Bailey", "Max", "Charlie", "Buddy", "Rocky", "Jake", "Jack",
    "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear",
    "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy",
    "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus",
    "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy",
    "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno",
    "Beau", "Dakota", "Maximus", "Henry", "Romeo", "Boomer", "Luke"
]

female_names = [
    'Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie',
    'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger',
    'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess', 'Emma',
    'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie',
    'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha',
    'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy',
    'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = [
    "http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct",
    "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct",
    "http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct",
    "http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct",
    "http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg",
    "http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct",
    "http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct",
    "http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct",
    "http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct",
    "http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

puppy_descriptions = [
    'Cute dog',
    'Nice Puppy',
    'Sweet little thing'
]

adopter_names = [
    'Miss Robinson',
    'Alex Jones',
    'Grandmar',
    'Louis Poulsen',
    'Henry The Fourth']


# This method will make a random age for each puppy between
# 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
    today = datetime.date.today()
    days_old = randint(0, 540)
    birthday = today - datetime.timedelta(days=days_old)
    return birthday


# This method will create a random weight between 1.0-40.0 pounds
# (or whatever unit of measure you prefer)
def CreateRandomWeight():
    return str(random.uniform(1.0, 40.0))


# This Method will create a random Profile and return the id of the description
def CreateRandomProfile():
    new_profile = Profile(
        picture=random.choice(puppy_images),
        description=random.choice(puppy_descriptions)
    )
    session.add(new_profile)
    session.commit()
    return new_profile.id


# This method will crete a new puppy
def createPuppy(name, gender):
    profile_id = CreateRandomProfile()
    new_puppy = Puppy(
        name=name,
        gender=gender,
        dateOfBirth=CreateRandomAge(),
        profile_id=profile_id,
        weight=CreateRandomWeight()
    )
    session.add(new_puppy)
    session.commit()
    print new_puppy.name


# This method will crete a new puppy
def createAdopter(name):
    new_adopter = Adopter(
        name=name,
    )
    session.add(new_adopter)
    session.commit()
    print new_adopter.name

# Create some males
for m_name in male_names:
    createPuppy(m_name, 'male')

# Create some females
for i, f_name in enumerate(female_names):
    createPuppy(f_name, 'female')

# Create all adopters
# for i, adopter_name in enumerate(adopter_names):
#     createAdopter(adopter_name)


# def createRandomAdoption():
#     randomPuppy = session.query(Puppy).order_by(func.random()).first()
#     randomAdopter = session.query(Adopter).order_by(func.random()).first()
#     randomAdopter.adopted_puppies.append(randomPuppy)
#     session.add(randomAdopter)
#     session.commit()
#     print '***** Adoption ***'
#     print "Adopter {0}".format(randomAdopter.name)
#     for puppie in randomAdopter.adopted_puppies:
#         print "Puppie {0}".format(puppie.name)

# Create some random adoptions
# for num in range(1,10):
#     createRandomAdoption()
