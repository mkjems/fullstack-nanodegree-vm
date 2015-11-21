-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS players, matches;

CREATE TABLE players (
 id serial PRIMARY KEY,
 name varchar(50) UNIQUE NOT NULL,
 dateCreated timestamp DEFAULT current_timestamp
);

-- INSERT INTO players (name) VALUES ('Martin');
-- INSERT INTO players (name) VALUES ('Henning');
-- INSERT INTO players (name) VALUES ('Lars');
-- INSERT INTO players (name) VALUES ('Torben');

select * from players;

CREATE TABLE matches (
 game_id serial PRIMARY KEY,
 winner integer,
 looser integer,
 dateCreated timestamp DEFAULT current_timestamp
);

INSERT INTO matches (winner, looser) VALUES (1, 2);
INSERT INTO matches (winner, looser) VALUES (3, 4);

select * from matches;

-- SELECT * FROM players JOIN matches ON (players.id = matches.winner) WHERE players.id = 2;

-- SELECT * FROM players JOIN matches ON (players.id = matches.winner) WHERE players.id = 2;
