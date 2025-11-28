import datetime
import bcrypt
from src import db
from flask import jsonify, request
from src.models.register_modal import Alumni
from src.models.user_model import User
from src.utils.jwt import decode_jwt_token, generate_jwt_token
from flask import send_file
from sqlalchemy import func

from src.controllers.register_controller import get_by_email

import os


def register_controller():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "User already exists", "success": 2})

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(
            username=username, password=hashed_password.decode("utf-8"), role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully", "status": 1}), 201

    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def login_controller(enroll_no, email):
    try:

        if not enroll_no or not email:
            return jsonify({
                "message": "enrollNumber and email are required",
                "status": 0
            }), 400

        # Fetch alumni user
        user = Alumni.query.filter_by(enrollNumber=enroll_no).first()
        print(user)
        if not user:
            return jsonify({"message": "Invalid credentials", "status": 0}), 401

        basic = user.personal_basic or {}
        saved_email = (basic.get("email") or "").strip().lower()

        if saved_email != email.strip().lower():
            return jsonify({"message": "Invalid credentials", "status": 0}), 401

        # --- JWT TOKENS ---
        access_token = generate_jwt_token(user.id)
        refresh_token = generate_jwt_token(user.id, is_refresh=True)

        # OPTIONAL: add refresh token column in Alumni model if needed
        # user.refresh_token = refresh_token
        # user.refresh_token_created_at = datetime.datetime.utcnow()
        # db.session.commit()

        return jsonify({
            "message": "Login successful",
            "status": 1,
            "success": True
        }), 200

    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500


def token_refresh_controller():

    try:

        refresh_token = request.headers.get("Authorization")
        if not refresh_token or not refresh_token.startswith("Bearer "):
            return (
                jsonify({"message": "Refresh token missing or invalid", "status": 0}),
                400,
            )

        refresh_token = refresh_token.split(" ")[1]

        identity = decode_jwt_token(refresh_token)
        user = User.query.filter_by(id=identity["user_id"]).first()

        if not user:
            return jsonify({"message": "User not found", "status": 0}), 404

        if refresh_token != user.refresh_token:
            return jsonify({"message": "Invalid refresh token", "status": 0}), 401

        new_access_token = generate_jwt_token(user.id)
        new_refresh_token = generate_jwt_token(user.id, is_refresh=True)

        user.refresh_token = new_refresh_token
        user.token_created_at = datetime.datetime.utcnow()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Access token refreshed",
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                    "status": 1,
                }
            ),
            200,
        )
    except Exception as e:
        return (jsonify({"success": 0, "error": str(e)}), 500)
    
def download_qr_controller(email=None, enroll_no=None):
    user = None
    print("🔥 email:", email)
    print("🔥 enroll_no:", enroll_no)
    # Lookup by email
    if email:
        email = email.strip().lower()
        user = get_by_email(email)
    print("🔥 user after email lookup:", user)

    # Lookup by enroll number
    if not user and enroll_no:
        print("🔥 enroll_no before strip:", enroll_no)
        enroll_no = str(enroll_no).strip()
        user = Alumni.query.filter_by(enrollNumber=enroll_no).first()
    print(user)
    if not user:
        return jsonify({
            "success": False,
            "message": "No matching user found"
        }), 404

    # QR filename = enrollNumber.png
    filename = f"{user.enrollNumber}.png"

    return jsonify({
        "success": True,
        "filename": filename,      # 🔥 return only filename
        "message": "QR filename fetched successfully"
    }), 200

