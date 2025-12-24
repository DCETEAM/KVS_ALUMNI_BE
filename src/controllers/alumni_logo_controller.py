from flask import request, jsonify
from src import db
from src.models.alumni_logo_selection import AlumniLogoSelection
from sqlalchemy import func

def save_alumni_logo():
    try:
        data = request.get_json()

        enroll_number = data.get("enrollNumber")
        selected_logo = data.get("selectedLogo")

        if not enroll_number or not selected_logo:
            return jsonify({
                "status": "error",
                "message": "Enroll number and selected logo are required"
            }), 400

        # Check if already selected
        record = AlumniLogoSelection.query.filter_by(
            enroll_number=enroll_number
        ).first()

        if record:
            return jsonify({
                "status": "error",
                "message": "You have already selected a logo"
            }), 409  # Conflict

        # Save new selection
        record = AlumniLogoSelection(
            enroll_number=enroll_number,
            selected_logo=selected_logo
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Logo selection saved successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to save logo selection",
            "error": str(e)
        }), 500


def get_logo_counts():
    try:
        results = (
            db.session.query(
                AlumniLogoSelection.selected_logo,
                func.count(AlumniLogoSelection.id).label("count")
            )
            .group_by(AlumniLogoSelection.selected_logo)
            .all()
        )

        counts = [
            {
                "logo": row.selected_logo,
                "count": row.count
            }
            for row in results
        ]

        return jsonify({
            "status": "success",
            "data": counts
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch logo counts",
            "error": str(e)
        }), 500
