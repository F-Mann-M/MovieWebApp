from flask import Flask, render_template
from models import db, Movie, User
from data_manager import DataManager
from sqlalchemy import select
import os


data_manager = DataManager()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def home():
    """Renders index.html and all"""
    return "wellcome to MovieWebApp"


@app.route('/users', methods=['POST'])
def get_user():
    # users = db.session.execute(db.select(User)).all() does not work with flask-sqlalchemy
    users = data_manager.get_users()
    return "<br>".join([user.name for user in users]) #just for testing


@app.route('/users/<int:user_id>/movies', methods=['GET'])


@app.route('/users/<int:user_id>/movies', methods=['POST'])


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])



if __name__ == "__main__":
    # create table
    with app.app_context():
        db.create_all()

    # run Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)