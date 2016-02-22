from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
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

# restaurants = session.query(Restaurant).all()
# for restaurant in restaurants:
#     print restaurant.name

count = session.query(Restaurant).count()
print 'Restaurants {0}'.format(count)

count = session.query(MenuItem).count()
print 'Items {0}'.format(count)

# first = session.query(Restaurant).first()
# print first.name

# items = session.query(MenuItem).order_by(MenuItem.name).all()
# for item in items:
    # print item.name

# #### Delete #####

# session.query(Restaurant).delete()
# session.commit()
# session.query(MenuItem).delete()
# session.commit()

veggie_burgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggie in veggie_burgers:
    print veggie.id
    print veggie.price
    print veggie.restaurant.name
    print "\n"

print "*************** Find item by id ******************\n"
urban_burger = session.query(MenuItem).filter_by(id = 9).one()
print urban_burger.id
print urban_burger.price
print urban_burger.restaurant.name

print "*************** Changing price of one ******************\n"
urban_burger.price = '$2.99'
session.add(urban_burger)
session.commit()

print "*************** Changing price of all veggies ******************\n"
for veggie in veggie_burgers:
    if veggie.price != '$2.99':
        veggie.price = '$2.99'
        session.add(veggie)
        session.commit()

print "*************** Delete item *******************"
try:
    nigiri = session.query(MenuItem).filter_by(name='Nigiri Sampler').one()
    print nigiri.name
    print nigiri.price
    session.delete(nigiri)
    session.commit()
except:
    print "No item named Nigiri Sampler found"
