from session import session
from database_model import Restaurant, Base, MenuItem, User

# Delete all existing
session.query(Restaurant).delete()
session.query(MenuItem).delete()
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
