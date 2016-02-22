run: db populate-db.made
	python project.py

populate-db: db populate-db.made

populate-db.made: database_populate.py
	python database_populate.py
	touch populate-db.made

db: restaurantmenu.db database_setup.py

restaurantmenu.db: database_setup.py
	python database_setup.py

clean:
	rm -f restaurantmenu.db
	rm -f populate-db.made
