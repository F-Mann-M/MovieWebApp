from models import db, User, Movie, movies_users
from dotenv import load_dotenv
import os, requests

load_dotenv()
API_KEY = os.getenv("API_KEY")


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
    def get_movies(self, user_id):
        """ get list of movies form movies table"""
        movies = db.session.query(Movie).all()
        return movies


    def add_movie(self, title, user_id):
        """ Add movie to database and link user to movie"""

        # Fetch movie from API
        movie_data = self.fetch_movie_data(title)

        if not movie_data:
            raise ValueError(f"Movie {title} no found!")

        # Get movie library
        existing = db.session.query(Movie).filter_by(title==movie_data.get("title")).first()
        if existing:
            raise ValueError(f"Movie {title} already in library!")

        # add movie to movies
        new_movie = Movie(
            title = movie_data.get("Title"),
            director = movie_data.get("director"),
            year = movie_data.get("Year"),
            poster_url = movie_data.get("Poster")
        )

        # Get user object from User
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Link user to movie
        user.movies.append(new_movie) #using movies_users helper table to link user to movie

        db.session.add(new_movie)
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


    def remove_movie_from_favorites(self, movie_id, user_id):
        """Removes link between movie_id and user_id"""
        # get user and movie object to session
        user = db.session.get(User, user_id)
        movie = db.session.get(Movie, movie_id)

        if not user or not movie:
            raise ValueError("Movie or user not found")

        if user in user.movies:
            user.movies.remove(movie)


    #API
    def fetch_movie_data(self, title):
        """takes in movie title, trys to fetch the movie data from omdbapi and returns data"""
        try:
            url = f"http://www.omdbapi.com/?apikey={API_KEY}={title}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Error: {e}")

