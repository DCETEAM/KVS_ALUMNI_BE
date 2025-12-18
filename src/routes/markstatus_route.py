from flask import Blueprint, request, jsonify
from src.controllers.markstatus_controller import get_mark_status, get_marktype_counts, get_marktype_details, save_mark_status

markstatus_routes = Blueprint("markstatus_routes", __name__, url_prefix="/api/v1/mark")


@markstatus_routes.route("/save", methods=["POST"])
def save_mark():
    try:
        data = request.get_json()

        enroll_no = data.get("enrollNumber")
        mark_type = data.get("markType")

        if not enroll_no or not mark_type:
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        response, code = save_mark_status(enroll_no, mark_type)
        return jsonify(response), code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@markstatus_routes.route("/get/<enroll_no>", methods=["GET"])
def get_mark(enroll_no):
    try:
        response, code = get_mark_status(enroll_no)
        return jsonify(response), code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@markstatus_routes.route("/status/<enroll_no>", methods=["GET"])
def get_status(enroll_no):
    try:
        response, code = get_mark_status(enroll_no)
        return jsonify(response), code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@markstatus_routes.route("/counts", methods=["GET"])
def marktype_counts():
    response, code = get_marktype_counts()
    return jsonify(response), code

@markstatus_routes.route("/details/<mark_type>", methods=["GET"])
def marktype_details(mark_type):
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("perPage", 10))
    search = request.args.get("search")

    response, code = get_marktype_details(
        mark_type=mark_type,
        page=page,
        per_page=per_page,
        search=search
    )

    return jsonify(response), code