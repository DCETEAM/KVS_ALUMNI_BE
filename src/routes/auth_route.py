from flask import Blueprint
from flask import request, jsonify
from src.controllers.auth_controller import (
    login_controller,
    register_controller,
    token_refresh_controller,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")





# Static user list (array)
USERS = [
    {
        "username": "admin",
        "password": "12345",
        "name": "Admin User"
    },
    {
        "username": "veeramani",
        "password": "98765",
        "name": "Veeramani Technical Lead"
    },
    {
        "username": "manager",
        "password": "11111",
        "name": "Manager Access"
    }
]


# Register route
@auth_bp.route("/register", methods=["POST"])
def register():
    return register_controller()


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        enroll_no = data.get("enrollNumber")
        email = data.get("email")

        if not enroll_no or not email:
            return jsonify({
                "status": "error",
                "message": "Missing enrollNumber or email"
            }), 400

        # Controller already returns (jsonify({...}), status)
        return login_controller(enroll_no, email)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@auth_bp.route("/staticlogin", methods=["POST"])
def staticlogin():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    print("🔥 Login attempt for user:", username)   
    print("🔥 Password provided:", password)

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and Password are required."
        }), 400

    # Find matching user from array
    matched_user = next(
        (u for u in USERS if u["username"] == username and u["password"] == password),
        None
    )

    if matched_user:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "name": matched_user["name"],
                "username": matched_user["username"]
            },
            "token": "STATIC-TOKEN-12345"
        }), 200

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401


# Token Refresh route
@auth_bp.route("/refresh", methods=["POST"])
def token_refresh():
    return token_refresh_controller()


# @user_bp.route("/", methods=["GET"])
# @token_required
# def get_user(decoded_payload):
#     return get_user_controller()
