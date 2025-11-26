from flask import request, jsonify, current_app
import jwt
import datetime
import bcrypt
from functools import wraps

SECRET_KEY = 'bB@&2VbxD!yT5q!lKj*Wn?I}5M6xZ$@^'
ALGORITHM = "HS256"


def generate_jwt_token(userid, is_refresh=False):
    expiration = datetime.datetime.utcnow() + (
        datetime.timedelta(days=7) if is_refresh else datetime.timedelta(seconds=30)
    )

    payload = {
        "user_id": userid,
        "type": "refresh" if is_refresh else "access",
        "exp": expiration,
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        token = token.split(" ")[1] if "Bearer" in token else token
        decoded_payload = decode_jwt_token(token)

        if not decoded_payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(decoded_payload, *args, **kwargs)

    return decorated
