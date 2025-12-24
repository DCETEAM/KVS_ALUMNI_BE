from flask import Blueprint
from src.controllers.alumni_logo_controller import save_alumni_logo,get_logo_counts

alumni_logo_bp = Blueprint(
    "alumni_logo_bp",
    __name__,
    url_prefix="/api/v1/logo"
)

@alumni_logo_bp.route("/save-logo", methods=["POST"])
def save_logo():
    return save_alumni_logo()

@alumni_logo_bp.route("/logo-counts", methods=["GET"])
def logo_counts():
    return get_logo_counts()
