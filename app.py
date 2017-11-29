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
    conn = movie.getConn()
    movies = movie.get_movies(conn)
    if request.method == 'POST':
        movie_tt = request.form['menu-tt']
        return redirect(url_for('update', id=movie_tt))
    return render_template('select.html')

@app.route('/make/', methods =['POST', 'GET'])
# page for making questions
def make():
    conn = movie.getConn()
    movie_data = movie.find_movie(conn, int(id))
    return render_template('make.html', data=update_info)

app.secret_key = 'youcantguessthisout'

@app.route('/quiz/<id>')
#page for taking a quiz
def quiz(id):
    return render_template('quiz.html')

if __name__ == '__main__':
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)

# did this work
