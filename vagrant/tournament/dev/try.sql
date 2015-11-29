
-- select p.name, count(m.winner) as wins
-- from players as p
-- left join matches as m on (m.winner = p.id)
-- group by p.name
-- order by wins desc;

-- select p.name, count(m.loser) as loses
-- from players as p
-- left join matches as m on p.id = m.loser
-- group by p.name;

-- select p.name, count(m.loser) as loses
-- from players as p
-- left join matches as m on p.id = m.loser
-- group by p.name;

select s3.name, s1.id, s1.losses , s2.wins , s1.losses + s2.wins as matches from

	(select p.id, count(m.loser) as losses from players as p
	left join matches as m on (p.id = m.loser) group by p.id order by p.id)
	as s1

	left join

	(select p2.id, count(m2.winner) as wins from players as p2
	left join matches as m2 on (p2.id = m2.winner) group by p2.id order by p2.id)
	as s2 on (s1.id = s2.id)

	join (select id, name from players)
	as s3 on (s1.id = s3.id)

	order by s2.wins desc;
