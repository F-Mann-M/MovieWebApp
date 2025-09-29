from models import db, User, Movie, movies_users
from sqlalchemy import select


class DataManager:
    # User management
    def create_user(self, name):
        """Add new user to users table"""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return f"User '{name}' was successfully added"


    def get_users(self):
        """get a list of users form users table"""
        users = db.session.query(User).all()
        return users


    def delete_user(self, user_id):
        """delete_user from users table"""
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return f"User {user.name} was successfully removed!"
        else:
            return "User not found database."


    # Movie management
    def get_movies(self):
        """ get list of movies form movies table"""
        movies = db.session.Query(Movie).all()
        return movies


    def add_movie(self, title, year, director, poster_url, user_id):
        """ Add movie to database and link user to movie"""
        # add movie to movies
        new_movie = Movie(title = title, year = year, director = director, poster_url = poster_url)

        # Get user object from User
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Link user to movie
        user.movies.append(new_movie) #using movies_users helper table to link user to movie

        db.session.add(Movie)
        db.session.commit()


    def update_movie(self, new_title, movie_id):
        """ takes in new title, director, year and movie_id, updates movie in database"""
        movie = db.session.get(Movie, movie_id)

        if not movie:
            raise ValueError(f"Movie with id {movie_id} not found")

        movie.title = new_title
        db.session.commit()



    def delete_movie(self, movie_id):
        """
        Takes in movie id and delete movie from database.
        Due to the many-to-many relationship the link between movies and users,
        the link between users and movies is automatically deleted
        """
        movie = db.session.get(Movie, movie_id)

        if not movie:
            raise ValueError(f"Movie with id {movie_id} not found")

        db.session.delete(movie)
        db.session.commit()