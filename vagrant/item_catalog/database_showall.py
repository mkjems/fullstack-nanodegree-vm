from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem, User

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
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

print '********* Users ***********'
users = session.query(User).all()
for user in users:
    print 'id:{} name:{}, picture:{}'.format(user.id, user.name, user.picture)

print '********* Restaurants ***********'
restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print 'id:{} name:{}'.format(restaurant.id, restaurant.name)

print '********* Menu Items ***********'
items = session.query(MenuItem).all()
for item in items:
    print 'id:{} name:{} restaurant:{}'.format(item.id, item.name, item.restaurant_id)
