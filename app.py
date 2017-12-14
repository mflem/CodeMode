# Maggie Jennings and Margaret Flemings
# CodeMode

from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session, send_from_directory
from werkzeug import secure_filename
import os, sys
import bcrypt
import MySQLdb
import codemodeFunctions
import dbconn2

app = Flask(__name__)

app.secret_key = 'youcantguessthisout'

#------ Login -----------------------

@app.route('/')
#login page
def index():
    return render_template('main.html', page_title='CodeMode: Welcome')

@app.route('/join/', methods=["POST"])
def join():
    try:
        username = request.form['username']
        passwd1 = request.form['password1']
        passwd2 = request.form['password2']
        if passwd1 != passwd2:
            flash('passwords do not match')
            return redirect( url_for('index'))
        hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
        conn = dbconn2.connect(dsn)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT loginname FROM users WHERE loginname = %s',
                     [username])
        row = curs.fetchone()
        if row is not None:
            flash('That username is taken')
            return redirect( url_for('index') )
        curs.execute('INSERT into users(loginname,password) VALUES(%s,%s)',
                     [username, hashed])
        session['username'] = username
        session['logged_in'] = True
        session['visits'] = 1
        return redirect( url_for('user', username=username) )
    except Exception as err:
        flash('form submission error '+str(err))
        return redirect( url_for('index') )

@app.route('/login/', methods=["POST"])
def login():
    try:
        username = request.form['username']
        passwd = request.form['password']
        conn = dbconn2.connect(dsn)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT password FROM users WHERE loginname = %s',
                     [username])
        row = curs.fetchone()
        if row is None:
            # Same response as wrong password, so no information about what went wrong
            flash('login incorrect. Try again or join')
            return redirect( url_for('index'))
        hashed = row['password']
        # strings always come out of the database as unicode objects
        if bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8')) == hashed:
            flash('successfully logged in as '+username)
            session['username'] = username
            session['logged_in'] = True
            session['visits'] = 1
            return redirect( url_for('user', username=username) )
        else:
            flash('login incorrect. Try again or join')
            return redirect( url_for('index'))
    except Exception as err:
        flash('form submission error '+str(err))
        return redirect( url_for('index') )


@app.route('/user/<username>')
def user(username):
    try:
        # don't trust the URL; it's only there for decoration
        if 'username' in session:
            username = session['username']
            session['visits'] = 1+int(session['visits'])
            return render_template('codemode.html',
                                   page_title='My App: Welcome '+username,
                                   name=username)
        else:
            flash('you are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

@app.route('/logout/')
def logout():
    try:
        if 'username' in session:
            username = session['username']
            session.pop('username')
            session.pop('logged_in')
            flash('You are logged out')
            return redirect(url_for('index'))
        else:
            flash('you are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )

#-------- End of Login Code ---------------


# @app.route('/home/')
# #home page
# def home(name):
#     return render_template('codemode.html', name=name)

@app.route('/select/', methods =['POST', 'GET'])
# page for selecting a deck to be quizzed on
def select():
    conn = codemodeFunctions.getConn()
    deckList = codemodeFunctions.getDeckList(conn)
    print deckList;
#     print [deckList];
    if request.method =='POST':
        deckid = request.form['decks']
        # using the deck's id, go to the associated quiz
        return redirect(url_for("quiz",deckid=deckid))
    return render_template('select.html', decks=deckList)

@app.route('/make/', methods =['POST', 'GET'])
# page for making questions to add to decks
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
            deckName = request.form['deckName']
            data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
            conn = codemodeFunctions.getConn()
            # insert returns the qid of the last inputted value on this connection
            newID = codemodeFunctions.insert(conn,data)
            return redirect(url_for("update",updateId=newID))
            # redirect to update page so updates can be made separately from make
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
                           deckName=qResults["deck_name"],
                           qtype=qResults["qtype"],
                           wrong1=qResults["wrong1"],
                           wrong2=qResults["wrong2"],
                           wrong3=qResults["wrong3"])

@app.route('/quiz/<deckid>', methods = ['POST', 'GET'])
#page for taking a quiz
def quiz(deckid):
    conn = codemodeFunctions.getConn()
    qResults = codemodeFunctions.getQuestionsFromDeck(conn, deckid)
    if request.method == 'POST':
        index = 0
        formData = []
        print request.form
        for q in qResults:
            qName = 'q[' + str(index) + ']'
            print request.form[qName]
            formData.append(request.form[qName])
            index += 1
        print formData
        answerResults = codemodeFunctions.gradeQuiz(conn, qResults, formData, 'me') # change to username later
        print answerResults
        return render_template('answeredQuiz.html', questions=qResults, results=answerResults)
    return render_template('quiz.html', questions=qResults)

if __name__ == '__main__':
  dsn = dbconn2.read_cnf()
  dsn['db'] = 'codemode_db'
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)
