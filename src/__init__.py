from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from .settings import KEY, TRACK_MODIFICATIONS, ENVIROMENT, DEBUG, DB_NAME

app = Flask(__name__)  # Create flask instance
db = SQLAlchemy()  # Create SQLAlchemy database
login_manager = LoginManager()  # Start login manager


def create_app():
    """Method to instantiate the application"""
    from .views import views
    from .db_views import db_views
    from .auth import auth
    from .models import User

    app.config['SECRET_KEY'] = KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRACK_MODIFICATIONS
    app.config['ENV'] = ENVIROMENT
    app.config['DEBUG'] = DEBUG
    app.config["CACHE_TYPE"] = "null"
    db.init_app(app)  # Instantiates the database

    app.register_blueprint(views, url_prefix='/')  # Adds view endpoints
    app.register_blueprint(db_views, url_prefix='/')  # Adds db_view endpoints
    app.register_blueprint(auth, url_prefix='/')  # Adds auth endpoints

    create_database(app)  # Creates new database

    login_manager.login_view = 'auth.login'  # Sets up login manager
    login_manager.init_app(app)  # Instantiates login manager

    @login_manager.user_loader  # Creates endpoint for login manager
    def load_user(user_id):
        """Function to load user"""
        return User.query.get(int(user_id))  # Returns the database query for given user

    return app  # Returns the application


def create_database(app):
    """Function to instantiate the database"""
    if not path.exists('src/' + DB_NAME):  # If the database does not exist
        db.create_all(app=app)  # Creates all tables found in .model
        print("Created Database")
