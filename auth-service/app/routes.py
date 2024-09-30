from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from .models import db, User
from .utils import generate_token
import time

auth_blueprint = Blueprint('auth', __name__)

# Function to handle retries
def retry_request(func, retries=3, *args, **kwargs):
    attempt = 0
    while attempt < retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            attempt += 1
            if attempt == retries:
                return jsonify({'message': f'Request failed after {retries} attempts: {str(e)}'}), 500
            time.sleep(1)  # Delay before retrying

# Register a new user (POST request)
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    new_user = User.query.filter_by(username=data['username']).first()
    if new_user:
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])

    # Add error handling with retries for database commit
    def commit_user():
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

    return retry_request(commit_user)

# Login a user (POST request)
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.hashed_password, data['password']):
        token = generate_token(user.id)

        def success_response():
            return jsonify({'message': 'Login successful', 'token': token}), 200

        # Add retries in case of issues generating the token
        return retry_request(success_response)
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Health check (GET request) - For testing
@auth_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({'message': 'Auth service is running'}), 200
