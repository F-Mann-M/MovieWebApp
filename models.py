from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

movies_users = db.Table(
    "movies_users", # table name
    db.Column("movies_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key = True)
)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    # use a helper table (movies_users) to link user_id to movie_id

    movies = db.relationship("Movie", secondary=movies_users, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"


class Movie(db.Model):
    __tablename__= "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String)

    # use helper table to link user to movie id
    users = db.relationship("User", secondary=movies_users, back_populates="movies")

    def __repr__(self):
        return f"<Movie(id={self.id}, name={self.title})>"