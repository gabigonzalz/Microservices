import jwt
from datetime import datetime, timedelta
import os  # Import os to use environment variables

def generate_token(user_id):
    # Use an environment variable for the secret key
    secret_key = os.getenv('JWT_SECRET_KEY', 'your_default_secret_key')  # Provide a default for local testing
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    # Try hashing the JWT token
    try:
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    except Exception as e:
        # Handle exceptions related to token generation
        print(f"Error generating token: {e}")  # Log the error
        return None
