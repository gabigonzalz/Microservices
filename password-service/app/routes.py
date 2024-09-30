# app/routes.py
from flask import Blueprint, request, jsonify, render_template
from .models import db, Password
from .utils import get_user_id_from_token

password_blueprint = Blueprint('password', __name__)

# Show new password form (GET request)
@password_blueprint.route('/new_password', methods=['GET'])
def show_new_password():
    return render_template('new_password.html')

# Add a new password (POST request)
@password_blueprint.route('/new_password', methods=['POST'])
def new_password():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or not data.get('service') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    # Create a new Password entry
    new_entry = Password(user_id=user_id, service=data['service'])
    new_entry.set_password(data['password'])  # Set the hashed password

    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({'message': 'Password added successfully'}), 201

# Show modify password form (GET request)
@password_blueprint.route('/modify_password', methods=['GET'])
def show_modify_password():
    return render_template('modify_password.html')

# Modify a password (POST request)
@password_blueprint.route('/modify_password', methods=['POST'])
def modify_password():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    modify_entry = Password.query.filter_by(user_id=user_id, service=data['service']).first()
    if modify_entry:
        modify_entry.set_password(data['new_password'])  # Set the new hashed password
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    else:
        return jsonify({'message': 'Password not found'}), 404

# Show list of passwords (GET request)
@password_blueprint.route('/list_passwords', methods=['GET'])
def list_passwords():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    passwords = Password.query.filter_by(user_id=user_id).all()
    return render_template('list_passwords.html', passwords=passwords)
