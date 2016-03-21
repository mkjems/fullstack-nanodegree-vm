

DATABASE_NAME=restaurantmenuwithusers.db
DATABASE_MODEL=item_catalog/db/database_model.py
DATABASE_POPULATE=item_catalog/db/database_populate.py
DATABASE_POPULATE_MADE=$(WD)item_catalog/db/populate-db.made
PYC=$(shell find . -name *.pyc )
UPLOADED_IMAGES=$(shell find \
		item_catalog/uploaded_images/ -maxdepth 1 -type f \
		| grep -v 'Burger.jpg' \
		| grep -v 'Icecream.jpg' | xargs)

run: db $(DATABASE_POPULATE_MADE)
	@python finalproject.py

populate-db: db $(DATABASE_POPULATE_MADE)

$(DATABASE_POPULATE_MADE): $(DATABASE_POPULATE)
	@python -m item_catalog.db.database_populate
	@touch $@

db: $(DATABASE_NAME) $(DATABASE_MODEL)

$(DATABASE_NAME): $(DATABASE_MODEL)
	@python -m item_catalog.db.database_model

clean:
	@rm -f $(DATABASE_NAME)
	@rm -f $(DATABASE_POPULATE_MADE)
	@rm -f $(PYC)
	@rm -f $(UPLOADED_IMAGES)

show-database:
	@python -m item_catalog.db.database_showall

show-database-sqlite3:
	@sqlite3 -batch -init item_catalog/db/database_commands.txt $(DATABASE_NAME)

