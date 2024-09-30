from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Stored user_id from the auth microservice
    service = db.Column(db.String(80), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)  # Renamed for clarity

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)  # Uses set_password method

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
