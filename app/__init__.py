from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()  # Declare db here

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Or your preferred database

    db.init_app(app)  # Initialize db with app
    login_manager.init_app(app)  # Initialize LoginManager with app

    from .models import User  # Import here to avoid circular import

    return app
