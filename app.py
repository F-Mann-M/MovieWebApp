from flask import Flask, render_template
from models import db, Movie, User
from data_manager import DataManager
import os


data_manager = DataManager()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def home():
    """Loads a list of users and renders index.html"""
    return "wellcome to MovieWebApp"


@app.route('/users', methods=['POST'])
def get_user():
    """Receives new user data, added it to users table, renders index.htm"""
    # users = db.session.execute(db.select(User)).all() does not work with flask-sqlalchemy
    users = data_manager.get_users()
    return "<br>".join([user.name for user in users]) #just for testing


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_users_movie(user_id):
    """Get users id and returns list of movies linked to the user_id"""
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Takes in new Movie. If movie not in list the movie is added to table movies
    and linked to the users id (via movies_users helper table)
    """



@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie():
    """Takes in movie id and title. if movie id in movies table updates title and renders index.html"""
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def remove_movie_from_favorites():
    """Removes link between user and movie id to remove it from users favour list. Movie stays in table movies"""
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def fetch_movie_data():
    """Fetch movie data from API"""
    pass



if __name__ == "__main__":
    # create table
    with app.app_context():
        db.create_all()

    # run Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)