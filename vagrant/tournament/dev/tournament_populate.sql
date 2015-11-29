
INSERT INTO players (name) VALUES ('Martin');
INSERT INTO players (name) VALUES ('Henning');
INSERT INTO players (name) VALUES ('Lars');
INSERT INTO players (name) VALUES ('Torben');
INSERT INTO players (name) VALUES ('Mark');
INSERT INTO players (name) VALUES ('Gregory');
INSERT INTO players (name) VALUES ('Philip');
INSERT INTO players (name) VALUES ('John');

-- SELECT * FROM players JOIN matches ON (players.id = matches.winner) WHERE players.id = 2;

INSERT INTO matches (winner, loser) VALUES (1, 2);
INSERT INTO matches (winner, loser) VALUES (3, 4);
