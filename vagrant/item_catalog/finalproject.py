from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# API endpoint
@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menuitem_id):
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    return jsonify(MenuItems=menuitem.serialize)


# API endpoint
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuitems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in menuitems])


# Root of website - all Restaurants
@app.route('/')
@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    # render_template('restaurantList.html', restaurants=restaurants)
    return 'List of all restaurants'


# Create a new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def restaurantCreate():
    return 'Create a new restaurant'


# Update Restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def restaurantUpdate(restaurant_id):
    return 'Edit a new restaurant'


# Delete Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def restaurantDelete(restaurant_id):
    return 'Delete restaurant'


# Menu of a single restaurant
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template(
        'restaurantMenu.html',
        restaurant=restaurant,
        items=items)


@app.route('/restaurants/<int:restaurant_id>/item/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New Menu Item created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template(
            'newMenuItem.html',
            restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuitem_id):
    menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menuitem.name = request.form['name']
        if request.form['description']:
            menuitem.description = request.form['description']
        if request.form['price']:
            menuitem.price = request.form['price']
        session.add(menuitem)
        session.commit()
        flash('Menu Item {0} Updated'.format(menuitem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editMenuItem.html',
            restaurant_id=restaurant_id,
            menuitem_id=menuitem_id,
            item=menuitem)


@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuitem_id):
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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
