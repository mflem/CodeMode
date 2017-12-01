# Maggie Jennings and Margaret Flemings
# CodeMode
# Draft

from flask import Flask, render_template, request, flash, redirect, url_for
import os, sys
import MySQLdb
import codemodeFunctions
import dbconn2

app = Flask(__name__)

@app.route('/')
#home page
def home():
    return render_template('codemode.html')

@app.route('/select/', methods =['POST', 'GET'])
# page for selecting a deck to quiz on
def select():
    conn = codemodeFunctions.getConn()
    deckList = codemodeFunctions.getDeckList(conn)
    return render_template('select.html', decks = deckList)

@app.route('/make/', methods =['POST', 'GET'])
# page for making questions
def make():
    if request.method == 'POST': # if there is a request
        action = request.form['submit']
        if action == 'submit':
            #gathers inputted info to send to database
            questionText = request.form['questionText']
            answer = request.form['answer']
            qtype = request.form['qtype']
            wrong1 = request.form['wrong1']
            wrong2 = request.form['wrong2']
            wrong3 = request.form['wrong3']
            explanation = request.form['explanation']
            pointVal = request.form['pointVal']
            deckNum = request.form['deckNum']
            data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckNum)
            conn = codemodeFunctions.getConn()
            newID = codemodeFunctions.insert(conn,data)
            # newIDStr = str(newID["qid"])
            return redirect(url_for("update",updateId=newID))
            # throw in redirect to update page
    else:
        return render_template('make.html')

@app.route('/update/<updateId>', methods =['POST', 'GET'])
# page for updating questions
def update(updateId):
    conn = codemodeFunctions.getConn()
    qResults = codemodeFunctions.getQuestion(conn, updateId)
    # print qResults["questionText"]
    return render_template('make.html',
                           questionText=qResults["questionText"],
                           answer=qResults["answer"],
                           explanation=qResults["explanation"],
                           pointVal=qResults["point_value"],
                           deckNum=qResults["deck_num"],
                           qtype=qResults["qtype"],
                           wrong1=qResults["wrong1"],
                           wrong2=qResults["wrong2"],
                           wrong3=qResults["wrong3"])


app.secret_key = 'youcantguessthisout'

@app.route('/quiz/<deckid>')
#page for taking a quiz
def quiz(deckid):
    conn = codemodeFunctions.getConn()
    qResults = codemodeFunctions.getQuestionsFromDeck(conn, deckid)
    return render_template('quiz.html', questions=qResults)

if __name__ == '__main__':
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)

# did this work
