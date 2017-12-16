# Margaret Flemings and Maggie Jennings
# CodeMode
# Draft 11/30/17

import sys
import MySQLdb
import dbconn2
from flask import flash

#functions and connections necessary for app.py

def insert(conn, data):
    #add a question into the database and return the newly inserted question's id
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        # data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
        # uses prepared query to avoid attacks
        curs.execute('''INSERT INTO questions
        (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
        to_flash = "Question (" + str(data[0]) +") was inserted successfully"
        flash(to_flash)
        # check the id of the last inserted question because the qid is auto incremented
        curs.execute('''SELECT last_insert_id();''')
        # fetch the row
        qID = curs.fetchone()
        #check the value in the row
        return qID["last_insert_id()"]
    except Exception as error:
        flash("error: {}".format(error))

def insertDeck(conn, deckName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    pathname = deckName + '.jpeg'
    try:
        curs.execute('''INSERT INTO decks
        (deck_name, image_path)
        VALUES(%s, %s)''', ([deckName, pathname]))
        to_flash = "Question (" + str(data[0]) +") was inserted successfully"
        flash(to_flash)
        # check the id of the last inserted question because the qid is auto incremented
        curs.execute('''SELECT last_insert_id();''')
        # fetch the row
        deckid = curs.fetchone()
        #check the value in the row
        return deckid["last_insert_id()"]
    except Exception as error:
        flash("error: {}".format(error))

def getQuestion(conn, inQid):
    # return question info given qid
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from questions where qid = %s;', [inQid])
    result = curs.fetchone()
    print result
    return result

def getDeckID(conn, deckName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT deckid from decks where deck_name = %s;', [deckName])
    result = curs.fetchone()
    return result

def getQuestionsFromDeck(conn, deck_num):
    # return array of all questions given a deck number
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from questions where deck_num = %s;', [deck_num])
    result = curs.fetchall()
    print result
    return result

def getDeckList(conn):
     # return all unique deck numbers
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT DISTINCT(deck_name) AS deck_name FROM decks ORDER BY deckid DESC;')
    result = curs.fetchall()
    deck_list = []
    for row in result:
        deck_list.append(row["deck_name"])
    print deck_list
    return deck_list

def getDeck(conn, deckNum):
    #returns all question ids for every question in a given deck
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT qid from questions where deck_num = %s;', [deckNum])
    return curs.fetchall()

def getConn():
    DSN = dbconn2.read_cnf('~/.my.cnf')
    DSN['db'] = 'codemode_db'
    conn = dbconn2.connect(DSN)
#     cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    return conn

def gradeQuiz(conn, questionInfo, formData, username):
    #grades the quiz and returns a list which can be used by the template
    #to show the proper responses and add up the proper amount of points
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #counters to keep track of the current question, points, num correct, etc
    index = 0;
    pointCounter = 0;
    answerResults = []; #using booleans to keep track of right/wrong answers
    totalCorrect = 0;
    for question in formData:
        if questionInfo[index]['answer'] == formData[index]: #if right answer
            pointCounter += questionInfo[index]['point_value'] #add points
            totalCorrect += 1 #increment correct
            answerResults.append(True)
        else:
            answerResults.append(False)
        index += 1
    #query to addpoints to the user's info in the database
    curs.execute('UPDATE users SET points = points + %s where loginname = %s;', [pointCounter, username])
    answerResults.append(totalCorrect) #add totalCorrect to the end so it can be displayed
    return answerResults
