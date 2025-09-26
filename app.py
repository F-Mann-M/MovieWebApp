from flask import Flask, render_template
from models import db
from data_manager import DataManager
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data/movies.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# create table
with app.app_context():
    db.create_all()

if __name__ == "__main__":

    # run app
    app.run(host="0.0.0.0", port=5000, debug=True)