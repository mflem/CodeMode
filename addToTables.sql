insert into users(loginname,points,email,isCollaborator,password) values
       ('Martha',0, 'martha@gmail.com','y','5551234'),
       ('Brandy',9,'martha@gmail.com','n','5550000'),
       ('Simba',0,'martha@gmail.com','n','5555555'),
       ('Suzy',0,'martha@gmail.com','n','5551234');

insert into questions(questionText, answer) values ('Is pi delicious?','Obviously');
insert into questions(questionText, answer) values ('How much wood would a woodchuck, chuck, if a woodchuck was Chuck Norris?', 'Much');

//1
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("How do you close an <html> tag?","</html>", "multi", "<html>", "/html", "<close html>", "You close tags with a slash '/' infront of the original tag",1,1)
//2
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("Which of the following is an inline element?","<span>", "multi", "<div>", "<li>", "<header>", "span is the only inline element",1,1)
//3
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("Which attribute do you use for links?","href", "style", "name", "value", "<close html>", "You can use the href attribute to make HTML links",1,1)

insert into madeBy(qid, cid) values 
		('1','2'),
		('3','2');

UPDATE questions SET wrong2 = 'Hardly' WHERE qid=1;

UPDATE questions SET wrong1 = '1' WHERE qid=2;
UPDATE questions SET wrong2 = '2' WHERE qid=2;
