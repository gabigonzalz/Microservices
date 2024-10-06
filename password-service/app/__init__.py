import asyncio
from flask import Flask
from .config import Config
from .models import db
from .messaging import subscribe_to_subject, close_nats

# NATS message handles
async def message_handler(msg):
    # Handle messages received from NATS
    data = msg.data.decode()
    print(f"Received a message: {data}")

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

    # Subscribe to NATS messages on startup
    loop = asyncio.get_event_loop()
    loop.create_task(subscribe_to_subject("auth-service.user.created", message_handler))

    # Define teardown logic inside create_app where `app` is defined
    @app.teardown_appcontext
    def shutdown_nats(exception=None):
        # Shutdown NATS connection when the app shuts down
        asyncio.run(close_nats())

    return app
