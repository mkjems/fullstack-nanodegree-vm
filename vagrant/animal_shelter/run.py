from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import desc, asc

from database_setup import Shelter, Base, Puppy, Adopter

engine = create_engine('sqlite:///puppyshelter.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

shelter_count = session.query(Shelter).count()
print 'Sheleters {0}'.format(shelter_count)

puppy_count = session.query(Puppy).count()
print 'Puppies {0}'.format(puppy_count)

print "\n** 1. Query all of the puppies and return the results in ascending alphabetical order **\n"
puppies = session.query(Puppy).order_by('name').all()
for puppy in puppies:
    print '{0} {1}'.format(puppy.id, puppy.name)

print "\n** 2. Query all of the puppies that are less than 6 months old organized by the youngest first **\n"
puppies = session.query(Puppy).filter(Puppy.dateOfBirth > '2015-09-17').order_by(desc(Puppy.dateOfBirth)).all()
for puppy in puppies:
    print '{0} {1} {2}'.format(puppy.id, puppy.name, puppy.dateOfBirth)

print "\n** 3. Query all puppies by ascending weight **\n"
puppies = session.query(Puppy).order_by(asc(Puppy.weight)).all()
for puppy in puppies:
    print '{0} {1}'.format(puppy.name, puppy.weight)

print "\n** 4. Query all puppies grouped by the shelter in which they are staying **\n"
puppies = session.query(Puppy).order_by(Puppy.shelter_id).all()
for puppy in puppies:
    print '{0} {1}'.format(puppy.name, puppy.shelter.name)
