from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from werkzeug.security import check_password_hash
from .models import db, User
from .utils import generate_token

auth_blueprint = Blueprint('auth', __name__)

# Show registration form (GET request)
@auth_blueprint.route('/register', methods=['GET'])
def show_register():
    return render_template('register.html')

# Register a new user (POST request)
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Expect JSON data
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    # Create a new user
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Show login form (GET request)
@auth_blueprint.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

# Login a user (POST request)
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Expect JSON data
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.hashed_password, data['password']):
        token = generate_token(user.id)  # Generate JWT token
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Redirect root to login page
@auth_blueprint.route('/', methods=['GET'])
def redirecting():
    return redirect(url_for('auth.show_login'))
