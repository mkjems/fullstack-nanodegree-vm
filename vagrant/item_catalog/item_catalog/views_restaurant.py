from item_catalog import app

from db import session
from db.database_model import Restaurant, MenuItem, User

from flask import session as login_session
from flask import render_template, request, redirect, url_for, flash, jsonify

from views_login import showLogin
from db.user import getUserInfo


# Root of website - all Restaurants Public
@app.route('/')
@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    print restaurants

    if 'username' not in login_session:
        return render_template(
            'restaurants-public.html',
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
        return render_template('new-restaurant.html')


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
        return render_template('edit-restaurant.html', restaurant=restaurant)


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
        return render_template('delete-restaurant.html', restaurant=restaurant)


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
            'restaurant-menu-public.html',
            restaurant=restaurant,
            appetizers=appetizers,
            main_dishes=main_dishes,
            beverages=beverages,
            desserts=desserts,
            creatorPicture=creator.picture
        )
    else:
        isCreator = login_session['user_id'] == creator.id
        return render_template(
            'restaurant-menu.html',
            restaurant=restaurant,
            appetizers=appetizers,
            main_dishes=main_dishes,
            beverages=beverages,
            desserts=desserts,
            isCreator=isCreator,
            creatorPicture=creator.picture
        )


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
