from flask import Flask
from .config import Config
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    # Initialize extensions
    db.init_app(app)

    # Register routes
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
