from app import create_app
from app.models import db

# Create an instance of the Flask app
app = create_app()

# Create the database tables within the app context
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
