
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


def restaurants_list_model():
    model = []
    all_restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    for restaurant in all_restaurants:
        model.append(restaurant)
    return model


def restaurant_create_model(name):
    new_restaurant = Restaurant(name=name)
    session.add(new_restaurant)
    session.commit()
    return


def restaurant_model(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return restaurant


def restaurant_update_model(restaurant_id, new_name):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurant.name = new_name
    session.add(restaurant)
    session.commit()
    return


def restaurant_delete(restaurant_id):
    print '** Model deleting {0} **'.format(restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print 'DELETING NAME: {0}'.format(restaurant.name)
    print 'DELETING ID: {0}'.format(restaurant.id)
    session.delete(restaurant)
    session.commit()
    return
