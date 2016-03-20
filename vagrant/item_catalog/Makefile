

DATABASE_NAME=restaurantmenuwithusers.db
DATABASE_MODEL=item_catalog/db/database_model.py
DATABASE_POPULATE=item_catalog/db/database_populate.py
DATABASE_POPULATE_MADE=$(WD)item_catalog/db/populate-db.made
PYC=$(shell find . -name *.pyc )

run: db $(DATABASE_POPULATE_MADE)
	python finalproject.py

populate-db: db $(DATABASE_POPULATE_MADE)

$(DATABASE_POPULATE_MADE): $(DATABASE_POPULATE)
	python -m item_catalog.db.database_populate
	touch $@

db: $(DATABASE_NAME) $(DATABASE_MODEL)

$(DATABASE_NAME): $(DATABASE_MODEL)
	python -m item_catalog.db.database_initialize

clean:
	rm -f $(DATABASE_NAME)
	rm -f $(DATABASE_POPULATE_MADE)
	rm -f $(PYC)

show-database:
	python -m item_catalog.db.database_showall

show-database-sqlite3:
	sqlite3 -batch -init item_catalog/db/database_commands.txt $(DATABASE_NAME)

run-locally: venv
	venv/bin/python finalproject.py

venv: venv/.made

venv/.made: requirements.txt
	virtualenv -p python2.7 venv
	venv/bin/pip install -r requirements.txt
	touch $@
