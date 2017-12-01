/* Data that can be inserted temporarily for testing purposes */

/* test users */
insert into users(loginname,points,email,isCollaborator,password) values
       ('Martha',0, 'martha@gmail.com','y','secret'),
       ('Brandy',9,'brandy@gmail.com','n','supersecret'),
       ('Simba',0,'simba@gmail.com','n','justcantwait'),
       ('Suzy',0,'suzi@gmail.com','n','imaspy');

//1
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("How do you close an <html> tag?","</html>", "multi", "<html>", "/html", "<close html>", "You close tags with a slash '/' infront of the original tag",1,1)
//2
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("Which of the following is an inline element?","<span>", "multi", "<div>", "<li>", "<header>", "span is the only inline element",1,1)
//3
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("Which attribute do you use for links?","href", "style", "name", "value", "<close html>", "You can use the href attribute to make HTML links",1,1)
//4
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("How do you comment in html?",
	"<!-- comment -->", "multi", "#comment", 
	"-- comment", "//comment", 
	'''<!-- --> is the correct format for commenting in html. 
	# allows commenting in Python. -- comments out in SQL. 
	Finally // works in Javascript.''',1,1)
//5
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num) 
VALUES("Which is a relative url?",
	"/kitten.png", "multi", "https://www.kittensinc.com/kitten.img", 
	"www.google.com/kitten.png", "Desktop/user/other/kitten.png", 
	'''The correct answer is /kitten.png because it does not specify the whole path.',1,1)
	
	
insert into madeBy(qid, cid) values 
		('1','2'),
		('3','2');


insert into questions(questionText, answer) values ('Is pi delicious?','Obviously');
insert into questions(questionText, answer) values ('How much wood would a woodchuck, chuck, if a woodchuck was Chuck Norris?', 'Much');

UPDATE questions SET wrong2 = 'Hardly' WHERE qid=1;

UPDATE questions SET wrong1 = '1' WHERE qid=2;
UPDATE questions SET wrong2 = '2' WHERE qid=2;
