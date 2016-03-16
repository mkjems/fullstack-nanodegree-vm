from session import session
from database_model import Restaurant, Base, MenuItem, User

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
