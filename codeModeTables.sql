-- includes users and collaborators who add new questions
drop table if exists users;
create table users (
       cid integer auto_increment primary key,
       loginname varchar(15) not null,
       points integer default 0,    
       email varchar(50) default null,     -- email address
       isCollaborator enum('y','n') default 'n', 
       password varchar(20)
       );


-- includes questions and answers as well as what they are worth
drop table if exists questions;
create table questions(
	qid integer auto_increment primary key,     
	questionText varchar(100),
	answer varchar(100),
	explanation varchar(500),     
	point_value integer,
	deck_num integer,
	qtype enum('multi','fillblank'), 
	wrong1 varchar(100), -- if not multi, NULL
	wrong2 varchar(100), -- if not multi, NULL
	wrong3 varchar(100) -- if not multi, NULL
       );

-- connects collaborators and the questions they made 
drop table if exists madeBy;
create table madeBy(
       qid integer foreign key,            
       cid integer foreign key,
       );

-- connects users with the questions they have answered 
drop table if exists hasAnswered;
create table hasAnswered(
       qid integer foreign key,            
       cid integer foreign key,
       );
       
       
