#-- starting with hw6 stuff

# Maggie Jennings and Margaret Flemings

from flask import Flask, render_template, request, flash, redirect, url_for
import os, sys
import MySQLdb
import movie as movie 
import dbconn2

app = Flask(__name__)

@app.route('/', methods =['POST', 'GET'])
def home():
    return render_template('hwk6.html')

@app.route('/search/', methods =['POST', 'GET'])
# renders search page, handles redirect to update based on user input
def search():
    if request.method == 'POST':
        title = request.form['search-title']
        if title == '':
            flash('error: please enter movie title')
            return render_template('search.html')
        else:
            conn = movie.getConn()
            new_title = "%" + title + "%" # allow for searching for similar titles         
            movie_tt = movie.searchId(conn, new_title)
            if movie_tt is None: # if no movie comes back from the database
                return render_template('search.html')
            else:
                return redirect(url_for('update', id=movie_tt['tt']))
    else:
        return render_template('search.html')

@app.route('/select/', methods =['POST', 'GET'])
# renders page with all movies without directors or release dates, redirects to update with selected movie's info
def select():
    conn = movie.getConn()
    movies = movie.get_movies(conn)
    if request.method == 'POST':
        movie_tt = request.form['menu-tt']
        return redirect(url_for('update', id=movie_tt))
    return render_template('select.html', movies = movies)

@app.route('/update/<id>', methods =['POST', 'GET'])
# renders update page with the info for the movie with the TT from the url
# allows for updates and deletions to the database
def update(id):
    conn = movie.getConn()
    movie_data = movie.find_movie(conn, int(id))
    if movie_data is None: # if user tries to direct to a tt that doesn't exist
        flash("Movie does not exist")
        return render_template('update.html')
    director_name = movie.get_director_name(conn, movie_data['director'])
    update_info = (movie_data['title'], movie_data['tt'],movie_data['release'],movie_data['director'],movie_data['addedby'], director_name)
    current_tt = movie_data['tt'] #save tt before to check if it has changed later
    if request.method == 'POST': # if there is a request
        action = request.form['submit']
        if action == 'update': 
            #gathers inputted info to send to database
            movie_title = request.form['movie-title']
            movie_tt = request.form['movie-tt']
            movie_release = request.form['movie-release']
            movie_director = request.form['movie-director']
            movie_addedby = request.form['movie-addedby']
            data = (movie_title, movie_tt, movie_release, movie_director, movie_addedby)
            if movie.doesMovieExist(conn,movie_tt) and current_tt != movie_tt: #if the movie already exists, we want to update but to re-render
                flash('Movie already exists')
                movie.update_movie(conn, data, current_tt)
                return render_template('update.html',data=data)
            else:  # otherwise update normally
                movie.update_movie(conn, data, current_tt)
            #re-render template since the TT is the same
            if (str(movie_tt) == str(current_tt)):
                return render_template('update.html', data=data)
            else: #if tt is different
                print 'redirected'
                return redirect(url_for('update', id=movie_tt))
        elif action == 'delete': 
            movie_tt = request.form['movie-tt']
            movie.delete_movie(conn, movie_tt)
            return redirect(url_for('home'))
    return render_template('update.html', data=update_info)

app.secret_key = 'youcantguessthisout'

if __name__ == '__main__':
  app.debug == True
  port = os.getuid()
  app.run('0.0.0.0', port)
