from item_catalog import app

from flask import session as login_session
from flask import render_template, request, redirect, url_for, flash

from db import session
from db.database_model import Restaurant, MenuItem
from db.user import getUserInfo

import constants
from login_required_decorator import login_required


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
            'new-menu-item.html',
            restaurant=restaurant,
            courses=constants.COURSES)


# Edit Menu Item
@app.route('/restaurants/<int:restaurant_id>/item/<int:menuitem_id>/edit', methods=['GET', 'POST'])
@login_required
def editMenuItem(restaurant_id, menuitem_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    if creator.id != login_session['user_id']:
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
            'edit-menu-item.html',
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
            'delete-menu-item.html',
            item=menuitem)
