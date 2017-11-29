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
    return render_template('select.html')

@app.route('/make/', methods =['POST', 'GET'])
# page for making questions
def make():

    return render_template('make.html', data=update_info)

app.secret_key = 'youcantguessthisout'

@app.route('/quiz/<id>')
#page for taking a quiz
def quiz(id):
    if request.method == 'POST': # if there is a request
        action = request.form['submit']
        if action == 'add':
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
            codemodeFunctions.update(conn,data)
            # throw in redirect to update page
    else:
        return render_template('quiz.html')

if __name__ == '__main__':
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)

# did this work
