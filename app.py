# Maggie Jennings and Margaret Flemings
# CodeMode

from flask import Flask, render_template, make_response, request, flash, redirect, url_for, session, send_from_directory, jsonify
from werkzeug import secure_filename
import os, sys
import bcrypt
import imghdr #for image file upload
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
        flash('Welcome to CodeMode, '+username+'.')
        flash('To get started you may like to chose a subject to be quizzed on.')
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
            flash('Welcome to CodeMode, '+username+'.')
            flash('To get started you may like to chose a subject to be quizzed on.')
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

@app.route('/pic/<fname>')
def pic(fname):
    f = secure_filename(fname)
    return send_from_directory('images',f)

@app.route('/select/', methods =['POST', 'GET'])
# page for selecting a deck to be quizzed on
def select():
    if 'username' not in session:
        return redirect( url_for('index') )
    else:
        username= session['username']
        conn = codemodeFunctions.getConn()
        deckList = codemodeFunctions.getDeckTotalList(conn)
        if request.method =='POST':
            deckName = request.form['selectDeck']
            deckid = codemodeFunctions.getDeckID(conn, deckName)
            deckid = deckid['deckid']
            # using the deck's id, go to the associated quiz
            return redirect(url_for("quiz", deckid=deckid))
        return render_template('select.html', decks=deckList,username=username)

# INSERT AND UPDATE questions --------------------------------------------------
@app.route('/insertQuestion/', methods =['POST', 'GET'])
# page for making questions to add to decks
def insertQuestion():
    if 'username' not in session:
        return redirect( url_for('index') )
    else:
        username= session['username']
        conn = codemodeFunctions.getConn()
        deckList = codemodeFunctions.getDeckList(conn)
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
                if (not questionText or not answer or (qtype == "multi" and (not wrong1 or not wrong2 or not wrong3)) or not explanation or pointVal <= 0 or not deckName):
                    flash("Please fill out all fields before submitting your question!")
                    data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
                    return render_template('insertQuestion.html', decks=deckList,username=username)
                else:
                    data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
                    conn = codemodeFunctions.getConn()
                    # insert returns the qid of the last inputted value on this connection
                    newID = codemodeFunctions.insertQuestion(conn,data)
                    return redirect(url_for("update",updateId=newID))
                # redirect to update page so updates can be made separately from insertQuestion
        else:
            return render_template('insertQuestion.html', decks=deckList,username=username)

@app.route('/update/<updateId>', methods =['POST', 'GET'])
# page for updating questions
def update(updateId):
    if 'username' not in session:
        return redirect( url_for('index') )
    else:
        username= session['username']
        conn = codemodeFunctions.getConn()
        qResults = codemodeFunctions.getQuestion(conn, updateId)
        deckList = codemodeFunctions.getDeckList(conn)
        print "what the info should be is: "
        print qResults
        currentDeckName = codemodeFunctions.getDeckName(conn, qResults["deck_num"])
        print "in update"
        if request.method == 'POST':
            if request.form['action'] == 'delete':
                codemodeFunctions.deleteQuestion(conn,updateId)
                return redirect(url_for('insertQuestion'))
            elif request.form['action'] =='update':
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
                if (not questionText or not answer or (qtype == "multi" and (not wrong1 or not wrong2 or not wrong3)) or not explanation or pointVal <= 0 or not deckName):
                    flash("Please fill out all fields before submitting your question!")
                    data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
                    return render_template('updateQuestion.html',
                                            questionText=questionText,
                                            answer=answer,
                                            explanation=explanation,
                                            pointVal=pointVal,
                                            selectedDeck=deckName,
                                            wrong1=wrong1,
                                            wrong2=wrong2,
                                            wrong3=wrong3,
                                            decks=deckList,
                                            username=username)
                else:
                    data = (questionText, answer, qtype, wrong1, wrong2, wrong3, explanation, pointVal, deckName)
                    conn = codemodeFunctions.getConn()
                    newInfo = codemodeFunctions.updateQuestion(conn,updateId,data)
                    return redirect(url_for("update",updateId=updateId))
        return render_template('updateQuestion.html',
                           questionText=qResults["questionText"],
                           answer=qResults["answer"],
                           explanation=qResults["explanation"],
                           pointVal=qResults["point_value"],
                           selectedDeck=currentDeckName,
                           qtype=qResults["qtype"],
                           wrong1=qResults["wrong1"],
                           wrong2=qResults["wrong2"],
                           wrong3=qResults["wrong3"],
                           decks=deckList,
                           username=username)

# INSERT AND UPDATE decks ------------------------------------------------------

@app.route('/insertDeck/', methods=['POST', 'GET'])
def addDeck():
    if 'username' not in session:
        return redirect( url_for('index') )
    else:
        username= session['username']
        conn = codemodeFunctions.getConn()
        if request.method == 'POST':
            deckName = request.form['deckName']
            if codemodeFunctions.getDeckID(conn, deckName):
                flash("Deck with the name " + deckName + " already exists!")
                return render_template('insertDeck.html',username=username)
            else:
                try:
                    f = request.files['imagefile']
                    mime_type = imghdr.what(f.stream)
                    if mime_type == 'jpeg' or mime_type == 'png' or mime_type == 'jpg':
                        filename = secure_filename(deckName + '.' + mime_type)
                        pathname = 'images/'+ filename
                        f.save(pathname)
                        flash('Upload successful')
                        url = url_for('pic',fname=filename)
                        newID = codemodeFunctions.insertDeck(conn, deckName, url)
                        return redirect(url_for('updateDeck', deckID=newID))
                    else:
                        raise Exception('Not a JPEG, JPG, or PNG')
                except Exception as err:
                    flash('Upload failed {why}'.format(why=err))
                    return render_template('insertDeck.html',username=username)
        else:
            return render_template('insertDeck.html',username=username)

@app.route('/updateDeck/<deckID>', methods=['POST', 'GET'])
def updateDeck(deckID):
    if 'username' not in session:
        return redirect( url_for('index') )
    else:
        username= session['username']
        conn = codemodeFunctions.getConn()
        deckInfo = codemodeFunctions.getDeckInfo(conn, deckID)
        deckID = deckInfo["deckid"]
        if request.method == 'POST':
            deckName = request.form['deckName']
            testDeckID = codemodeFunctions.getDeckID(conn, deckName)
            if testDeckID and (testDeckID != deckID):
                    flash("Deck with name " + deckName + " already exists!")
            else:
                codemodeFunctions.updateDeck(conn, deckName, deckID)
                return redirect(url_for('updateDeck', deckID))
        return render_template('updateDeck.html',username=username,deckInfo=deckInfo)

@app.route('/quiz/<deckid>', methods = ['POST', 'GET'])
#page for taking a quiz
def quiz(deckid):
    if 'username' not in session:
        return redirect( url_for('index') )
    else:
        username= session['username']
        conn = codemodeFunctions.getConn()
        qResults = codemodeFunctions.getQuestionsFromDeck(conn, deckid)
        if request.method == 'POST':
        #"counts" through list of questions to collect data from each question
        # in the form submitted, which in turn gives back to the new page
            index = 0
            formData = []
            for q in qResults:
                # print request.form
                qName = 'q[' + str(index) + ']'
                formData.append(request.form[qName])
                index += 1
            answerResults = codemodeFunctions.gradeQuiz(conn, qResults, formData, user) # change to username later
            return render_template('answeredQuiz.html', questions=qResults, results=answerResults, form=formData,username=username)
        return render_template('quiz.html', questions=qResults, username=username)

if __name__ == '__main__':
  dsn = dbconn2.read_cnf()
  dsn['db'] = 'codemode_db'
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)
