from flask import request, jsonify
import jwt
import os  # Import os to use environment variables

def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None  # Return None if there's no auth header
    
    try:
        # Assuming 'Bearer <token>'
        token = auth_header.split(' ')[1]
        secret_key = os.getenv('JWT_SECRET_KEY', 'your_default_secret_key')  # Use the same secret key
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])  # Use the secret key from env variable
        return payload['user_id']
    except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print(f"Error decoding token: {e}")  # Log the error
        return None
