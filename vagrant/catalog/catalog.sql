
-- CREATE DATABASE catalog;

-- Connect to the catalog database
\c catalog;


CREATE TABLE catagories (
	id serial PRIMARY KEY,
	name varchar(50) UNIQUE NOT NULL
);

CREATE TABLE items (
	id serial PRIMARY KEY,
	title varchar(50) UNIQUE NOT NULL,
	description varchar(255),
	category int references catagories(id)
);

-- Create some dummy data

INSERT INTO catagories (name) VALUES ('Socccer');
INSERT INTO catagories (name) VALUES ('Basketball');
INSERT INTO catagories (name) VALUES ('Baseball');

select * from catagories;

INSERT INTO items (title, description, category )VALUES ('Ball', 'Nice for playing socccer.', 1);
INSERT INTO items (title, description, category )VALUES ('Basketball shoes', 'Nice for playing basketball.', 2);
INSERT INTO items (title, description, category )VALUES ('Baseball cap', 'Nice for a sunny day.', 1);

select * from items;
