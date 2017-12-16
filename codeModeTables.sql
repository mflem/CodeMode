-- includes users and collaborators who add new questions
drop table if exists users;
create table users (
       cid integer auto_increment primary key,
       loginname varchar(15) not null,
       points integer default 0,
       email varchar(50) default null,     -- email address
       isCollaborator enum('y','n') default 'n',
       password varchar(150)
       );

drop table if exists hasAnswered;
create table decks(
       	deckid integer auto_increment primary key,
        deck_name varchar(100) not null,
      	image_path varchar(100),
        );

-- includes questions and answers as well as what they are worth
drop table if exists questions;
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

-- connects collaborators and the questions they made
drop table if exists madeBy;
create table madeBy(
	qid int not null,
	cid int,
	index(qid),
	index(cid),
	foreign key (qid) references questions(qid) on delete restrict,
	foreign key (cid) references users(cid) on delete restrict
       );


-- connects users with the questions they have answered
drop table if exists hasAnswered;
create table hasAnswered(
	qid int not null,
	cid int not null,
	index(qid),
	index(cid),
	foreign key (qid) references questions(qid) on delete restrict,
	foreign key (cid) references users(cid) on delete restrict
       );
