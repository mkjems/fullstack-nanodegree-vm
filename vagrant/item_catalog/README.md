
[![Flask Project](http://flask.pocoo.org/static/badges/flask-project-s.png)](http://flask.pocoo.org)

#Item Catalog

This is my submission to the Udacity Full Stack Developer course 'Item Catalog' project.
This is a restaurant menu website that allows users to log in using their Google+
account via oAuth. Once authenticated, users can manage menu cards
of restaurants they create.

## 1. Running the code from a Vagrant virtual machine
This is a Python Flask project running of Sql Lite.
If you have [Virtualbox](https://www.virtualbox.org/) and [Vagrant](http://vagrantup.com/)
installed you can run the project like so:

First clone this repo and start the virtual machine and ssh into it.

	git clone git@github.com:mkjems/fullstack-nanodegree-vm.git
	cd fullstack-nanodegree-vm/vagrant/
	vagrant up
	vagrant ssh

Once you are inside the virtual machine:

	cd /vagrant/item_catalog
	make run

`make run` will poppulate the database and start the webserver.
You should then be able to view the Restaurant website on [http://localhost:5000](http://localhost:5000)


## 2. Requirements

The project relies on [these requirements](requirements.txt).


## 3. Usage

The website has 8 different screens, that hopefully are self explainatory.
After you login using the login button on the top right.
It is possible to create, edit and delete restaurants.
It is also possible to create, edit and delete menu items for the restaurants you create.
It is possible to read the menus of restaurants other users created.

These are the url endpoints of the website:

	restaurants/
	restaurants/new
	restaurants/<restaurant_id>/edit
	restaurants/<restaurant_id>/delete

	restaurants/<restaurant_id>/menu
	restaurants/<restaurant_id>/menu/JSON

	restaurants/<restaurant_id>/item/<item_id>/edit
	restaurants/<restaurant_id>/item/<item_id>/delete
	restaurants/<restaurant_id>/item/<item_id>/JSON
	restaurants/<restaurant_id>/item/new

There are also two endpoints to get the menu data in json form.

## 4. Features

- Protection against CSRF attacks
- Image upload for menu items
