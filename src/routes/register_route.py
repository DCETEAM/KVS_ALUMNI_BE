from flask import Blueprint, request, jsonify
import json
from sqlalchemy import cast, String

from src.controllers.register_controller import create_alumni, get_all, get_by_enroll_number, get_by_id, update_alumni

alumni_routes = Blueprint("alumni_routes", __name__, url_prefix="/api/v1/register")

# -------------------------------------------------------------
# CREATE ALUMNI (POST)
# -------------------------------------------------------------
@alumni_routes.route("/alumni", methods=["POST"])
def create_route():
    try:
        raw_json = request.form.get("jsonData")
        file = request.files.get("file") 

        if not raw_json:
            return jsonify({"status": "error", "message": "jsonData missing"}), 400

        data = json.loads(raw_json)

        result = create_alumni(data, file)

        return jsonify({
            "status": "success",
            "message": "Registered successfully",
            "id": result.id,
            "enrollNumber": result.enrollNumber
        }), 201

    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        print("🔥 CREATE ERROR:", e)
        return jsonify({"status": "error", "message": "Server error"}), 500




# -------------------------------------------------------------
# GET ALL ALUMNI (GET)
# -------------------------------------------------------------
@alumni_routes.route("/alumni", methods=["GET"])
def get_all_route():
    try:
        rows = get_all()
        serialized = [row.serialize() for row in rows]

        return jsonify({
            "status": "success",
            "count": len(serialized),
            "data": serialized
        }), 200

    except Exception as e:
        print("🔥 GET ALL ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------------------------------------
# GET ALUMNI BY ID (GET)
# -------------------------------------------------------------
@alumni_routes.route("/alumni/<int:alumni_id>", methods=["GET"])
def get_by_id_route(alumni_id):
    try:
        row = get_by_id(alumni_id)
        if not row:
            return jsonify({
                "status": "error",
                "message": "Not Found"
            }), 404

        # Extract ONLY required fields
        personal = row.personal_basic or {}

        data = {
            "id": row.id,
            "enrollNumber": row.enrollNumber,
            "fullName": personal.get("fullName"),
            "email": personal.get("email"),
            "mobile": personal.get("mobile"),
            "profileImage": row.profileAssetPath
        }

        return jsonify({
            "status": "success",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@alumni_routes.route("/alumni/enroll/<string:enroll_no>", methods=["GET"])
def get_by_enroll_route(enroll_no):
    try:
        row = get_by_enroll_number(enroll_no)

        if not row:
            return jsonify({
                "status": "error",
                "message": "Not Found"
            }), 404

        data = {col.name: getattr(row, col.name) for col in row.__table__.columns}

        return jsonify({
            "status": "success",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------------------------------------------------
# UPDATE ALUMNI (PUT/PATCH) - use enrollNumber instead of internal id
# -------------------------------------------------------------
@alumni_routes.route("/updateAlumni/<string:enroll_no>", methods=["PUT"])
def update_route(enroll_no):
    try:
        raw_json = request.form.get("jsonData")
        file = request.files.get("file")

        print(raw_json)

        if not raw_json:
            return jsonify({"status": "error", "message": "jsonData missing"}), 400

        data = json.loads(raw_json)

        result = update_alumni(enroll_no, data, file)

        return jsonify({
            "status": "success",
            "message": "Updated successfully",
            "id": result.id,
            "enrollNumber": result.enrollNumber
        }), 200

    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        print("🔥 UPDATE ERROR:", e)
        return jsonify({"status": "error", "message": "Server error"}), 500



