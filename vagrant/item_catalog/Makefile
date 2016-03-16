WD=$(shell pwd)/

DATABASE_DIR=$(WD)item_catalog/db/
DATABASE_NAME=/vagrant/item_catalog/item_catalog/db/restaurantmenuwithusers.db
DATABASE_SETUP=$(WD)item_catalog/db/database_model.py
DATABASE_POPULATE=$(WD)item_catalog/db/database_populate.py
DATABASE_POPULATE_MADE=$(WD)item_catalog/db/populate-db.made

run: db $(DATABASE_POPULATE_MADE)
	python finalproject.py

populate-db: db $(DATABASE_POPULATE_MADE)

$(DATABASE_POPULATE_MADE): $(DATABASE_POPULATE)
	cd $(DATABASE_DIR); python ./database_populate.py
	touch $@

db: $(DATABASE_NAME) $(DATABASE_SETUP)

$(DATABASE_NAME): $(DATABASE_SETUP)
	cd $(DATABASE_DIR); python ./database_initialize.py

clean:
	rm -f $(DATABASE_NAME)
	rm -f $(DATABASE_POPULATE_MADE)

show-database:
	python item_catalog/db/database_showall.py

show-database-sqlite3:
	sqlite3 -batch -init item_catalog/db/database_commands.txt $(DATABASE_NAME)

run-locally: venv
	venv/bin/python finalproject.py

venv: venv/.made

venv/.made: requirements.txt
	virtualenv -p python2.7 venv
	venv/bin/pip install -r requirements.txt
	touch $@
