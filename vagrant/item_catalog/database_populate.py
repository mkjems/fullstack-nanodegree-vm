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

# Delete all existing

session.query(Restaurant).delete()
session.commit()
session.query(MenuItem).delete()
session.commit()
session.query(User).delete()
session.commit()

# ############  Create new ones ############

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Restaurant UrbanBurger
restaurant1 = Restaurant(user_id=1, name="Urban Burger")
session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(
       user_id=1,
       name="French Fries",
       description="with garlic and parmesan",
       price="$2.99",
       course="Appetizers",
       restaurant=restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
       user_id=1,
       name="Chicken Burger",
       description="Juicy grilled chicken burger with tomato mayo and lettuce",
       price="$5.50",
       course="Main Dish", restaurant=restaurant1)

session.add(menuItem2)
session.commit()
print "Added stuff to database!"
