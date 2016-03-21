import os

from werkzeug import secure_filename

from login_required_decorator import login_required

from flask import session as login_session
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory

from db import session
from db.database_model import Restaurant, MenuItem
from db.user import getUserInfo

import constants

from item_catalog import app
from item_catalog import ALLOWED_EXTENSIONS

from csrf_decorator import csrf_protect


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Create menu item
@app.route('/restaurants/<int:restaurant_id>/item/new', methods=['GET', 'POST'])
@csrf_protect
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    if ('username' not in login_session) or (creator.id != login_session['user_id']):
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        # File upload
        filename = ""
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newItem = MenuItem(
            course=request.form['course'],
            description=request.form['description'],
            name=request.form['name'],
            price=request.form['price'],
            restaurant_id=restaurant_id,
            user_id=login_session['user_id'],
            image=filename
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
@csrf_protect
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
@csrf_protect
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
