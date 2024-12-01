from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Add this line to specify the login view

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['DEBUG'] = True

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app