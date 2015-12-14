
test: db test-basic test-rematch

db: tournament_db.made
tournament_db.made: tournament.sql
	@psql -f tournament.sql
	@touch tournament_db.made

test-rematch: db test-rematch.made
test-rematch.made: tournament_rematch_tests.py
	@python tournament_rematch_tests.py
	@touch test-rematch.made

test-basic: db test-basic.made
test-basic.made: tournament_test.py
	@python tournament_test.py
	@touch test-basic.made

simulation: db
	@python tournament_simulation.py

clean:
	rm -f *.made

clean-tests:
	rm -f test-rematch.made test-basic.made simulation.made
