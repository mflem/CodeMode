# Margaret Flemings and Maggie Jennings
# CodeMode

import sys
import MySQLdb
import dbconn2
from flask import flash, session

#functions and connections necessary for app.py

def insertQuestion(conn, data):
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

def updateQuestion(conn, qid, data):
    #update a question in the database, returns the row for the updated question
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        # data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
        # uses prepared query to avoid attacks
        curs.execute('''UPDATE questions
        SET questionText = %s, answer = %s, qtype = %s, wrong1 = %s, wrong2 = %s, wrong3 = %s, explanation = %s, point_value = %s, deck_num = %s
        WHERE qid = %s''', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], qid))
        to_flash = "Question (" + str(data[0]) +") was inserted successfully"
        flash(to_flash)
        return getQuestion(conn, qid)
    except Exception as error:
        flash("error: {}".format(error))

def deleteQuestion(conn,qid):
    #function to delete a question from a deck given a question ID
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('DELETE FROM questions where qid = %s;', [qid])
    flash('Delete successful')

def insertDeck(conn, deckName, pathname):
    #function to insert a deck into the table, takes in the connection,
    #deckName, and URL and returns the ID of the newly inserted deck
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        curs.execute('''INSERT INTO decks
        (deck_name, image_path)
        VALUES(%s, %s)''', ([deckName, pathname]))
        to_flash = "Deck (" + deckName +") was updated successfully"
        flash(to_flash)
        # check the id of the last inserted question because the qid is auto incremented
        curs.execute('''SELECT last_insert_id();''')
        # fetch the row
        deckid = curs.fetchone()
        #check the value in the row
        return deckid["last_insert_id()"]
    except Exception as error:
        flash("error: {}".format(error))

def updateDeck(conn, deckName, deckNum):
    # function that takes in connection and deck info and updates the deck in
    #the decks table
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    pathname = deckName + '.jpeg'
    try:
        curs.execute('''UPDATE decks
        SET deck_name = %s
        WHERE deckid = %s''', ([deckName, deckNum]))
        to_flash = "Deck (" + deckName +") was updated successfully"
        flash(to_flash)
        return getDeckInfo(conn,deckNum)
    except Exception as error:
        flash("error: {}".format(error))

def getQuestion(conn, inQid):
    # return question info given qid
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from questions where qid = %s;', [inQid])
    result = curs.fetchone()
    return result

def getDeckID(conn, deckName):
    #takes in deck's name and returns the deck's ID
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT deckid from decks where deck_name = %s;', [deckName])
    result = curs.fetchone()
    return result

def getDeckName(conn, deckID):
    #takes in the deck's ID and returns the deck's name
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT deck_name from decks where deckid = %s;', [deckID])
    result = curs.fetchone()
    return result

def getQuestionsFromDeck(conn, deck_num):
    # return array of all questions given a deck number
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from questions where deck_num = %s;', [deck_num])
    result = curs.fetchall()
    return result

def getDeckList(conn):
     # return all unique deck numbers
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT DISTINCT(deck_name) AS deck_name FROM decks ORDER BY deckid DESC;')
    result = curs.fetchall()
    deck_list = []
    for row in result:
        deck_list.append(row["deck_name"])
    return deck_list

def getDeckTotalList(conn):
    #get all deck info for all decks
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM decks ORDER BY deckid DESC;')
        result = curs.fetchall()
        return result

def getDeck(conn, deckNum):
    #returns all question ids for every question in a given deck
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT qid from questions where deck_num = %s;', [deckNum])
    return curs.fetchall()

def getDeckInfo(conn, deckNum):
    #returns all info about a deck given the ID
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from decks where deckid = %s;', [deckNum])
    return curs.fetchone()

def getConn():
    DSN = dbconn2.read_cnf('~/.my.cnf')
    DSN['db'] = 'codemode_db'
    conn = dbconn2.connect(DSN)
    return conn

def gradeQuiz(conn, questionInfo, formData, username):
    #grades the quiz and returns a list which can be used by the template
    #to show the proper responses and add up the proper amount of points
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #counters to keep track of the current question, points, num correct, etc
    index = 0;
    pointCounter = 0;
    answerResults = []; # creating list of booleans to keep track of right/wrong answers (True = Correct, False = Incorrect)
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
    oldPoints = session['points']
    session['points'] = oldPoints + pointCounter
    answerResults.append(totalCorrect) #add totalCorrect to the end so it can be displayed
    return answerResults
