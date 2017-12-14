/* Data that can be inserted temporarily for testing purposes */
/* test users */
insert into users(loginname,points,email,isCollaborator,password) values
       ('Martha',0, 'martha@gmail.com','y','secret'),
       ('Brandy',9,'brandy@gmail.com','n','supersecret'),
       ('Simba',0,'simba@gmail.com','n','justcantwait'),
       ('Suzy',0,'suzi@gmail.com','n','imaspy');

INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("How do you close an <html> tag?","</html>", "multi", "<html>", "/html", "<close html>", "You close tags with a slash '/' infront of the original tag",1,"HTML");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("Which of the following is an inline element?","<span>", "multi", "<div>", "<li>", "<header>", "span is the only inline element",1,"HTML");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("Which attribute do you use for links?","href", "style", "name", "value", "<close html>", "You can use the href attribute to make HTML links",1,"HTML");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("How do you comment in html?",
	"<!-- comment -->", "multi", "#comment",
	"-- comment", "//comment",
	'''<!-- --> is the correct format for commenting in html.
	# allows commenting in Python. -- comments out in SQL.
	Finally // works in Javascript.''',1,"HTML Questions");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("Which is a relative url?",
	"/kitten.png", "multi", "https://www.kittensinc.com/kitten.img",
	"www.google.com/kitten.png", "Desktop/user/other/kitten.png",
	'''The correct answer is /kitten.png because it does not specify the whole path.',1,"HTML Questions");

/* SQL DECK */
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("What does SQL stand for?","Structured Query Language", "multi", "Structured Question Language", "Strong Query Language", "Sanctioned Query Language", "SQL stands for Structured Query Language",1,"SQL");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("Which SQL statement is used to update data in a database?","UPDATE", "multi", "INSERT", "MODIFY", "SAVE AS", "UPDATE is the keyword to update data in SQL.",1,"SQL");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("Which SQL statement is used to insert new data in a database?","INSERT INTO", "fillblank", "", "", "", "You use INSERT INTO to insert data into a table",2,"SQL");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("With SQL, how do you select all the columns from a table named Persons?",
	"SELECT * FROM Persons", "multi", "SELECT Persons",
	"SELECT *.Persons", "SELECT [all] FROM Persons",
	"SELECT * FROM Persons is the only valid answer.",3,"SQL");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("With SQL, how do you select a column named FirstName from a table named Persons?",
	"SELECT FirstName FROM Persons", "multi", "EXTRACT FirstName FROM Persons",
	"SELECT Persons.FirstName", "INSERT INTO Persons FirstName",
	"In SQL, you use the SELECT keyword to select columns from a table.",4,"SQL");

INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("What does PHP stand for?","PHP: Hypertext Preprocessor", "multi", "Private Home Page", "Personal Hypertext Processor", "Pigs Hugging Pugs", "",1,"PHP");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("PHP server scripts are surrounded by delimiters, which?","<?php...?>", "multi", "<script>...</script>", "<&>...</&>", "<?php>...</?>", "PHP is delimitted by <?php...?>",1,"PHP");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("How do you write Hello World in PHP?","echo...", "multi", "Document.Write(...);", "Hello World", "Hello.World", "echo is the proper way to put things back on a page.",2,"PHP");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("All variables in PHP start with which symbol?",
	"$", "fillblank", "#",
	"@", "%",
	"All variables in PHP start with $.",3,"PHP");
INSERT INTO questions(questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_name)
VALUES("How do you get information from a form that is submitted using the get method?",
	"$_GET[];", "multi", "$GET_REQUEST",
	"Request.Form;", "Request.QueryString;",
	"$_GET[]; is how you get information from the GET method request.",5,"PHP");
