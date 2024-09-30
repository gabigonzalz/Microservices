# app/__init__.py
from flask import Flask
from .config import Config
from .models import db

def create_app():
    # Flask settings
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    # Initialize extensions
    db.init_app(app)

    # Register routes
    from .routes import password_blueprint
    app.register_blueprint(password_blueprint)

    return app
