import jwt
from functools import wraps
from flask import request, jsonify
import os
from repos.users import get_user


SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise ValueError("Invalid token type")

            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = get_user(payload['sub'])

        except (ValueError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated_function
