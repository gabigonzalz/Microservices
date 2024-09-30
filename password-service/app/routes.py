# app/routes.py
from flask import Blueprint, request, jsonify
from .models import db, Password
from .utils import get_user_id_from_token
import time

password_blueprint = Blueprint('password', __name__)

# Utility function for retries
def retry(func, retries=3, delay=2):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e

# Add a new password (POST request)
@password_blueprint.route('/new_password', methods=['POST'])
def new_password():
    user_id = get_user_id_from_token()
    # Check for the JWT token
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    # Check for correct user input
    if not data or not data.get('service') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    # New password entry into the database
    def create_password_entry():
        new_entry = Password(user_id=user_id, service=data['service'])
        new_entry.set_password(data['password'])  # Set the hashed password
        db.session.add(new_entry)
        db.session.commit()

    try:
        retry(create_password_entry)  # Retry creating password entry if necessary
        return jsonify({'message': 'Password added successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Modify a password (POST request)
@password_blueprint.route('/modify_password', methods=['POST'])
def modify_password():
    user_id = get_user_id_from_token()
    # Check for the JWT token
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    # Check for correct user input
    if not data or not data.get('service') or not data.get('new_password'):
        return jsonify({'message': 'Invalid input'}), 400

    # Modify password entry in the database
    def modify_password_entry():
        modify_entry = Password.query.filter_by(user_id=user_id, service=data['service']).first()
        if modify_entry:
            modify_entry.set_password(data['new_password'])  # Set the new hashed password
            db.session.commit()
            return True
        else:
            return False

    try: # Try to modify the database entry
        if retry(modify_password_entry):
            return jsonify({'message': 'Password updated successfully'}), 200
        else:
            return jsonify({'message': 'Password not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Delete a password (DELETE request)
@password_blueprint.route('/delete_password', methods=['DELETE'])
def delete_password():
    user_id = get_user_id_from_token()
    # Check for the JWT token
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    # Check for correct user input
    if not data or not data.get('service'):
        return jsonify({'message': 'Invalid input'}), 400

    # Delete password entry from the database
    def delete_password_entry():
        delete_entry = Password.query.filter_by(user_id=user_id, service=data['service']).first()
        if delete_entry:
            db.session.delete(delete_entry)
            db.session.commit()
            return True
        else:
            return False

    try: # Try to delete the database entry
        if retry(delete_password_entry):
            return jsonify({'message': 'Password deleted successfully'}), 200
        else:
            return jsonify({'message': 'Password not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# List all passwords (GET request)
@password_blueprint.route('/list_passwords', methods=['GET'])
def list_passwords():
    user_id = get_user_id_from_token()
    # Check for the JWT token
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    # Get all the passwords of the user from the database
    def fetch_passwords():
        return Password.query.filter_by(user_id=user_id).all()

    try: # Try to get all the passwords and present them
        passwords = retry(fetch_passwords)
        return jsonify([
            {'service': p.service, 'hashed_password': '***'}  # Masking password for security
            for p in passwords
        ]), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Health check (GET request)
@password_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({'message': 'Password service is running'}), 200
