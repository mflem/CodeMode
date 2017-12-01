# Margaret Flemings and Maggie Jennings
# CodeMode
# Draft 11/30/17

import sys
import MySQLdb
import dbconn2
from flask import flash

#functions and connections necessary for app.py

def insert(conn, data):
    #add a question into the database
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        # data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckNum)
        print "we are trying"
        curs.execute('''INSERT INTO questions
        (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, point_value, deck_num)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
        to_flash = "Question (" + str(data[0]) +") was inserted successfully"
        flash(to_flash)
        # "insert into person VALUES(%s, %s, %s, %s)"
        curs.execute('''SELECT last_insert_id();''')
        qID = curs.fetchone()
        print qID
        print qID["last_insert_id()"]
        return qID["last_insert_id()"]
    except Exception as error:
        flash("error: {}".format(error))

def getQuestion(conn, inQid):
    #return question info
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from questions where qid = %s;', [inQid])
    result = curs.fetchone()
    print result
    return result

def getDeckList(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    result = curs.execute('SELECT DISTINCT(deck_num) AS deck_num FROM questions ORDER BY deck_num DESC;')
    print result
    return result

def getDeck(conn, decknum):
    #returns all question ids for every question in a given deck
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT qid from questions where deckNum = %s;', [decknum])
    return curs.fetchhall()

def getConn():
    DSN = dbconn2.read_cnf('~/.my.cnf')
    DSN['db'] = 'codemode_db'
    conn = dbconn2.connect(DSN)
#     cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    return conn
