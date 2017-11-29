# Maggie Jennings and Margaret Flemings
# CodeMode
# Draft

from flask import Flask, render_template, request, flash, redirect, url_for
import os, sys
import MySQLdb
import codemodeFunctions
import dbconn2

app = Flask(__name__)

@app.route('/', methods =['POST', 'GET'])
def home():
    return render_template('codemode.html')

@app.route('/select/', methods =['POST', 'GET'])
# renders page with all movies without directors or release dates, redirects to update with selected movie's info
def select():
    conn = movie.getConn()
    movies = movie.get_movies(conn)
    if request.method == 'POST':
        movie_tt = request.form['menu-tt']
        return redirect(url_for('update', id=movie_tt))
    return render_template('select.html', movies = movies)

@app.route('/make', methods =['POST', 'GET'])
# renders update page with the info for the movie with the TT from the url
# allows for updates and deletions to the database
def update(id):
    conn = movie.getConn()
    movie_data = movie.find_movie(conn, int(id))
    return render_template('update.html', data=update_info)

app.secret_key = 'youcantguessthisout'

if __name__ == '__main__':
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)

# did this work
