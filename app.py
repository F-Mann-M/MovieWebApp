from flask import Flask, render_template, request, redirect, flash, url_for
from models import db, Movie, User
from data_manager import DataManager
from dotenv import load_dotenv
import os
load_dotenv()

data_manager = DataManager()
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = os.getenv("FLASK_KEY") # need a kee to redirect messages in a get method


@app.route("/flash_test")
def flash_test():
    message = "This is a test flash message!"
    flash(message)
    return redirect(url_for("index"))

@app.route("/")
def index():
    """Loads a list of users and renders index.html"""
    users = data_manager.get_users()
    return render_template("index.html", users=users, title="Users")


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """Get users id and returns list of movies linked to the user_id"""
    movies = data_manager.get_movies(user_id)
    user = data_manager.get_user(user_id)
    if not movies:
        message = "Movie list empty"
    else:
        message = f"{user.name}'s Movies"
    return render_template("movies.html", message=message, user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Takes in new Movie. If movie not in list the movie is added to table movies
    and linked to the users id (via movies_users helper table)
    """
    title = request.form.get("title")
    user = data_manager.get_user(user_id)
    message = data_manager.add_movie(title, user_id)
    movies = data_manager.get_movies(user_id)
    flash(message) # use flash to keep the message even using a GET method for redirect
    return redirect(url_for("get_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Takes in movie id and title. if movie id in movies table updates title and renders index.html"""
    title = request.form.get("title")
    message = data_manager.update_movie(title, movie_id)
    flash(message)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def remove_movie_from_favorites(movie_id, user_id):
    """Removes link between user and movie id to remove it from users movie list. Movie stays in table movies"""
    message = data_manager.remove_movie_from_favorites(movie_id, user_id)
    flash(message)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/create_user", methods=["POST"])
def create_user():
    message = ""
    name = request.form.get("name")

    if name:
        message = data_manager.create_user(name)
    users = data_manager.get_users()
    return render_template("index.html", message=message, users=users, title="Users")



if __name__ == "__main__":
    # create table
    with app.app_context():
        db.create_all()

    # run Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)