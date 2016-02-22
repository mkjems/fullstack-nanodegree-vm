run: db pop
	python run.py

run2: db pop
	python run2.py

clean:
	rm -f puppyshelter.db
	rm -f pop.made

db: puppyshelter.db

puppyshelter.db: database_setup.py
	python database_setup.py

pop: db pop.made

pop.made:
	python populator.py
	touch pop.made

