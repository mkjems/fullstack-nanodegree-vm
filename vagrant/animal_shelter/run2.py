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

print '************ Status ***********'
shelter_count = session.query(Shelter).count()
print 'Sheleters {0}'.format(shelter_count)

puppy_count = session.query(Puppy).count()
print 'Puppies {0}'.format(puppy_count)

# #########
puppy = session.query(Puppy).filter_by(id='9').one()
print 'Puppy id 9 weight :{0}'.format(puppy.weight)


print '************* find all shelters ***********'
shelters = session.query(Shelter).all()
for shelter in shelters:
    print '************'
    print shelter.name
    print "Maximum capacity {0}".format(shelter.maximum_capacity)
    shelter_puppies = session.query(Puppy).filter_by(shelter_id=shelter.id)
    print 'Shelter as id:{0} and has {1} puppies'.format(
        shelter.id, shelter_puppies.count())
    for p in shelter_puppies:
        print '    {0}'.format(p.name)
