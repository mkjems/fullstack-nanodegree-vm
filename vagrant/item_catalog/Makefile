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

run-locally: venv
	venv/bin/python finalproject.py

venv: venv/.made

venv/.made: requirements.txt
	virtualenv -p python2.7 venv
	venv/bin/pip install -r requirements.txt
	touch $@
