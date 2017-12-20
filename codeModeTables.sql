drop table if exists questions;
drop table if exists decks;
drop table if exists users;

-- includes users and collaborators who add new questions
create table users (
       cid integer auto_increment primary key,
       loginname varchar(15) not null,
       points integer default 0,
       password varchar(150)
       );


create table decks(
       	deckid integer auto_increment primary key,
        deck_name varchar(100) not null,
      	image_path varchar(100)
        );

-- includes questions and answers as well as what they are worth
create table questions(
	qid integer auto_increment primary key,
	questionText varchar(100),
	answer varchar(100),
	explanation varchar(500),
	point_value integer,
	deck_num integer references decks(deckid) on delete restrict,
	qtype enum('multi','fillblank'),
	wrong1 varchar(100), -- if not multi, NULL
	wrong2 varchar(100), -- if not multi, NULL
	wrong3 varchar(100) -- if not multi, NULL
       );
