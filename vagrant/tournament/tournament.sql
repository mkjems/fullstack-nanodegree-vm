-- Table definitions for the tournament project.

-- Connect to the tournament database
\c tournament;

-- Delete the tables and views if they exit
DROP VIEW IF EXISTS history, standings CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

-- There are 2 tables

CREATE TABLE players (
	id serial PRIMARY KEY,
	name varchar(50) UNIQUE NOT NULL
);

CREATE TABLE matches (
	game_id serial PRIMARY KEY,
	winner integer references players(id),
	loser integer references players(id),
	dateCreated timestamp DEFAULT current_timestamp
);

-- And 4 views

-- This is the standings view

--        name        | id | losses | wins | matches
-- -------------------+----+--------+------+---------
-- Twilight Sparkle   |  1 |      0 |    1 |       1
-- Mister X           |  4 |      0 |    1 |       1
-- ...
CREATE VIEW standings AS
    select s3.name, s1.id, s1.losses , s2.wins , s1.losses + s2.wins as matches from

    (select p.id, count(m.loser) as losses from players as p
    left join matches as m on (p.id = m.loser) group by p.id order by p.id)
    as s1

    left join

    (select p2.id, count(m2.winner) as wins from players as p2
    left join matches as m2 on (p2.id = m2.winner) group by p2.id
    order by p2.id)

    as s2 on (s1.id = s2.id)

    join (select id, name from players)
    as s3 on (s1.id = s3.id)

    order by s2.wins desc;


-- This is the history view.
-- It can be used to easily find previous oponents

--  player | oponent |        datecreated
-- --------+---------+----------------------------
--      17 |      18 | 2015-12-08 21:33:13.89332
--      17 |      21 | 2015-12-08 21:33:14.480578
--      18 |      17 | 2015-12-08 21:33:13.89332
--      18 |      29 | 2015-12-08 21:33:14.120394
-- ...
CREATE VIEW history AS
	(select
		distinct player, w.loser as oponent, w.datecreated as datecreated
	from (
		select winner as player from matches
		union all
		select loser as player from matches
	) p

	join matches w on (w.winner = player)
	)

	union all

	(select
		distinct player, l.winner as oponent , l.datecreated as datecreated
	from (
		select winner as player from matches
		union all
		select loser as player from matches
	) p

	join matches l on (l.loser = player)
	)

	order by player, datecreated;


-- Finds oponents that have the same number of wins and matches
-- excludes rematches.

-- id  | oponent_id
-- -----+------------
--  110 |        120
--  110 |        122
--  110 |        123
--  111 |        113
CREATE VIEW posible_oponents AS
	select
		s.id, o.id as oponent_id
	from standings s
		join
		standings o on (
			s.wins = o.wins
			and s.matches = o.matches
			and o.id != s.id
			and o.id not in (select oponent from history where player = s.id)
		)
	order by id
	;

-- This is used to find the pairing for the next round.
-- It's just the posible_oponents view with an extra wins column

-- id  | oponent_id | wins
-- -----+------------+------
--  123 |        120 |    1
--  122 |        120 |    1
--  110 |        123 |    1
--  110 |        120 |    1
CREATE VIEW posible_games AS
	select
		po.id, po.oponent_id, s.wins
	from posible_oponents po
	join standings s on (s.id = po.id)
		order by wins
	;





