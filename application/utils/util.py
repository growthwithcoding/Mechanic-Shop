# application/utils/util.py
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from jose import jwt
import jose

SECRET_KEY = "a super secret, secret key"


def encode_token(customer_id):
    """
    Generate a JWT token for a customer.
    
    Args:
        customer_id: The unique identifier for the customer
        
    Returns:
        A JWT token string
    """
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),  # Expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at
        'sub': str(customer_id)  # Subject (customer_id as string)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    """
    Decorator to protect routes that require token authentication.
    
    The decorator:
    1. Extracts the token from the Authorization header
    2. Validates and decodes the token
    3. Passes the customer_id to the wrapped function
    
    Usage:
        @blueprint.route('/protected')
        @token_required
        def protected_route(customer_id):
            # customer_id is automatically provided by the decorator
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Look for the token in the Authorization header
        if 'Authorization' in request.headers:
            try:
                # Expected format: "Bearer <token>"
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid Authorization header format. Expected: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = int(data['sub'])  # Extract customer_id from the token
            
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        except (KeyError, ValueError):
            return jsonify({'message': 'Malformed token payload!'}), 401
        
        # Pass customer_id to the wrapped function
        return f(customer_id, *args, **kwargs)
    
    return decorated
