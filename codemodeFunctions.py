# Margaret Flemings and Maggie Jennings
# CodeMode
# Draft 11/30/17

import sys
import MySQLdb
import dbconn2
from flask import flash

#functions and connections necessary for app.py

def update_movie(conn, data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        # data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckNum)
        curs.execute('''INSERT INTO questions
        (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckNum)
                        ''', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
            to_flash = "Question (" + str(data[0]) +") was inserted successfully"
            flash(to_flash)
    except Exception as error:
        flash("error: {}".format(error))
