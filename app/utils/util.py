from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or "Mechanic Shop"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            if not token:
                return jsonify({"message": "Missing token"}), 401
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                member_id = data['sub']
                print(member_id)
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'Token is expired'}), 401
            except jose.exceptions.JWTError as e:
                print("Invalid Token:", e)
                return jsonify({'message': 'Invalid token'}), 401

            return f(member_id, *args, **kwargs)

        else:
            return jsonify({"message": "You must be logged in to access"}), 401
        
    return decorated