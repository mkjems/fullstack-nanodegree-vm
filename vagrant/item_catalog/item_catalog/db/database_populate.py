from session import session
from database_model import Restaurant, Base, MenuItem, User

# Delete all existing
session.query(Restaurant).delete()
session.query(MenuItem).delete()
session.query(User).delete()
session.commit()

# ############  Create new ones ############

# Create dummy user
User1 = User(name="Diner Jack", email="jack@diner.com",
             picture='http://localhost:5000/static/diner-owner.jpg')
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
       image="Burger.jpg",
       course="Main Dish", restaurant=restaurant1)

session.add(menuItem2)
session.commit()

menuItem2 = MenuItem(
       user_id=1,
       name="Ice cream Sundae",
       description="Classic ice cream dessert with chocolate souce",
       price="$4.50",
       image="Icecream.jpg",
       course="Main Dish", restaurant=restaurant1)

session.add(menuItem2)
session.commit()
print "Added stuff to database!"
