from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem, User

from flask import session as login_session
import random
import string

# Step 5vGconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# my stuff
import constants

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Database, connect and create session
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# login
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')


# login via Google+
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state' != login_session['state']):
        response = make_response(json.dumps('Invalid state !'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code to a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the acces token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-type'] = 'application/json'
    # Verify that the access token is for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID doesn't match app's."), 401)
        print "Token's client ID doesn't match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Centent-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists in database. If not make a new one
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    return output


# DISCONNECT Google+ - reset a users token and reset their login session
@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')

    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke current token
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset users session
        if 'credentials' in login_session:
            del login_session['credentials']
        if 'username' in login_session:
            del login_session['username']
        if 'picture' in login_session:
            del login_session['picture']

        response = make_response(json.dumps('Disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect(url_for('restaurantList'))

    else:
        # Something went wrong
        response = make_response(json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# API endpoint for single menu item of a restaurant
@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menuitem_id):
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    return jsonify(MenuItems=menuitem.serialize)


# API endpoint for a menu
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuitems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in menuitems])


# API endpoint for all restaurants
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


# Root of website - all Restaurants Public
@app.route('/')
@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    if 'username' not in login_session:
        return render_template(
            'restaurants_public.html',
            restaurants=restaurants
        )
    else:
        current_user = getUserInfo(login_session['user_id'])
        return render_template(
            'restaurants.html',
            restaurants=restaurants,
            user_id=login_session['user_id'],
            picture=current_user.picture
        )


# Create a new Restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def restaurantCreate():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'], user_id=login_session['user_id'])
        session.add(restaurant)
        session.commit()
        flash('New restaurant: {0} created!'.format(restaurant.name))
        return redirect(url_for('restaurantList'))
    else:
        return render_template('newRestaurant.html')


# Update a Restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def restaurantUpdate(restaurant_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    if (creator.id != login_session['user_id']):
        return '''<script>
        function myFunction(){
            alert('You are not authorized');
            location.href='/login';}
            </script>
            <body onload='myFunction();'>
        '''
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('Restaurant {0} Updated'.format(restaurant.name))
        return redirect(url_for('restaurantList'))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)


# Delete a Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def restaurantDelete(restaurant_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurantToDelete.user_id)
    if (creator.id != login_session['user_id']):
        return '''<script>
        function myFunction(){
            alert('You are not authorized');
            location.href='/login';}
            </script>
            <body onload='myFunction();'>
        '''
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        flashMessage = 'Restaurant: %s deleted!' % restaurant.name
        session.delete(restaurant)
        session.commit()
        flash(flashMessage)
        return redirect(url_for('restaurantList'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)


# Menu of a single restaurant (Public)
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)

    appetizers = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, course="Appetizers")
    main_dishes = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, course="Main Dish")
    beverages = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, course="Beverages").all()
    desserts = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, course="Desserts")

    if 'username' not in login_session:
        return render_template(
            'restaurantMenu_public.html',
            restaurant=restaurant,
            appetizers=appetizers,
            main_dishes=main_dishes,
            beverages=beverages,
            desserts=desserts,
        )
    else:
        isCreator = login_session['user_id'] == creator.id
        return render_template(
            'restaurantMenu.html',
            restaurant=restaurant,
            appetizers=appetizers,
            main_dishes=main_dishes,
            beverages=beverages,
            desserts=desserts,
            isCreator=isCreator
        )


# Create menu item
@app.route('/restaurants/<int:restaurant_id>/item/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    if ('username' not in login_session) or (creator.id != login_session['user_id']):
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        newItem = MenuItem(
            course=request.form['course'],
            description=request.form['description'],
            name=request.form['name'],
            price=request.form['price'],
            restaurant_id=restaurant_id,
            user_id=login_session['user_id']
        )
        session.add(newItem)
        session.commit()
        flash('New Menu Item created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template(
            'newMenuItem.html',
            restaurant=restaurant,
            courses=constants.COURSES)


# Edit Menu Item
@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    if ('username' not in login_session) or (creator.id != login_session['user_id']):
        return redirect(url_for('showLogin'))
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menuitem.name = request.form['name']
        if request.form['description']:
            menuitem.description = request.form['description']
        if request.form['price']:
            menuitem.price = request.form['price']
        if request.form['course']:
            menuitem.course = request.form['course']
        session.add(menuitem)
        session.commit()
        flash('Menu Item {0} Updated'.format(menuitem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editMenuItem.html',
            restaurant_id=restaurant_id,
            menuitem_id=menuitem_id,
            item=menuitem,
            courses=constants.COURSES)


# Delete menu item
@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuitem_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    if ('username' not in login_session) or (creator.id != login_session['user_id']):
        return redirect(url_for('showLogin'))
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        flashMessage = 'Menu item: %s deleted!' % menuitem.name
        session.delete(menuitem)
        session.commit()
        flash(flashMessage)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deleteMenuitem.html',
            item=menuitem)


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
