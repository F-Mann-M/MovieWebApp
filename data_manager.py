from models import db, User, Movie

class DataManager():

    def __init__(self):
        pass

    # User management
    def creat_user(self, name):
        """Add new user to users table"""
        user = User(name = name)
        db.session.commit()
        return f"User '{name}' was successfully added"


    def get_users(self):
        """get a list of users form users table"""
        users = db.session.execute(select(User)).scalar().all() # returns a list of row objects
        return users


    def delete_user(self, user_id):
        """delete_user from users table"""
        user = db.session.Query(User).filter(User.id == user_id).first()

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


    def add_movie(self, movie, user_id):
        """ Add movie to database"""
        new_movie = Movie(movie)


    def add_movie_to_user(self, user_id, movie_id):
        """Adds movie to users movie list by adding user and movie id to movies_users"""
        user = db.session(insert(User))



    def update_movie(self, new_title, movie_id):
        """ takes in new title, director, year and movie_id, updates movie in database"""
        pass


    def delete_movie(self, movie_id):
        """ Takes in movie id and delete movie from database"""
        pass