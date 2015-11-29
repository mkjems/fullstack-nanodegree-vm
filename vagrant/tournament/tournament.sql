-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS players, matches;

CREATE TABLE players (
	id serial PRIMARY KEY,
	name varchar(50) UNIQUE NOT NULL
);

CREATE TABLE matches (
	game_id serial PRIMARY KEY,
	winner integer,
	loser integer,
	dateCreated timestamp DEFAULT current_timestamp
);

