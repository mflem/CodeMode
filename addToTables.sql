insert into users(loginname,points,email,isCollaborator,password) values
       ('Martha',0, 'martha@gmail.com','y','5551234'),
       ('Brandy',9,'martha@gmail.com','n','5550000'),
       ('Simba',0,'martha@gmail.com','n','5555555'),
       ('Suzy',0,'martha@gmail.com','n','5551234');

insert into questions(questionText, answer) values ('Is pi delicious?','Obviously');
insert into questions(questionText, answer) values ('How much would would a woodchuck, chuck, if a woodchuck was Chuck Norris?', 'Much');

insert into madeBy(qid, cid) values 
		('1','2'),
		('3','2');

UPDATE questions SET wrong2 = 'Hardly' WHERE qid=1;

UPDATE questions SET wrong1 = '1' WHERE qid=2;
UPDATE questions SET wrong2 = '2' WHERE qid=2;
