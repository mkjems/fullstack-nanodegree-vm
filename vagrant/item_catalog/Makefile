DATABASE_NAME = restaurantmenuwithusers.db

run: db populate-db.made
	python finalproject.py

populate-db: db populate-db.made

populate-db.made: database_populate.py
	python database_populate.py
	touch populate-db.made

db: $(DATABASE_NAME) database_setup.py

$(DATABASE_NAME): database_setup.py
	python database_setup.py

clean:
	rm -f $(DATABASE_NAME)
	rm -f populate-db.made

show-database:
	python database_showall.py
