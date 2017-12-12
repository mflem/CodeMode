#!/usr/local/bin/python2.7

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory)
from werkzeug import secure_filename
app = Flask(__name__)

import os
import bcrypt
import MySQLdb
import dbconn2

app.secret_key = 'able baker charlie'

@app.route('/')
def index():
    return render_template('main.html', page_title='My App: Welcome')

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
        hashed = row['hashed']
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
            return render_template('greet.html',
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


if __name__ == '__main__':
    dsn = dbconn2.read_cnf()
    dsn['db'] = 'codemode_db'
    app.debug = True
    app.run('0.0.0.0',os.getuid())
