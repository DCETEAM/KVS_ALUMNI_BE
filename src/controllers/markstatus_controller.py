from src import db
from src.models.markstatus_modal import MarkStatus
from src.models.register_modal import Alumni

def save_mark_status(enroll_no, mark_type):
    """
    mark_type → Entry / Food / Kit Bag
    """

    # Check alumni exists
    alumni = Alumni.query.filter_by(enrollNumber=enroll_no).first()
    if not alumni:
        return {"status": "error", "message": "Invalid Enrollment Number"}, 404

    # Prevent duplicate marking for same category
    existing = MarkStatus.query.filter_by(
        enrollNumber=enroll_no,
        markType=mark_type
    ).first()

    if existing:
        return {"status": "error", "message": f"Already marked for {mark_type}"}, 409

    record = MarkStatus(
        enrollNumber=enroll_no,
        markType=mark_type
    )

    db.session.add(record)
    db.session.commit()

    return {
        "status": "success",
        "message": f"Marked as {mark_type} successfully",
        "data": record.serialize()
    }, 201

def get_mark_status(enroll_no):
    try:
        record = MarkStatus.query.filter_by(enroll_no=enroll_no).order_by(MarkStatus.id.desc()).first()

        if not record:
            return {"status": "not_found"}, 404

        return {
            "status": "success",
            "data": {
                "enrollNumber": record.enroll_no,
                "markType": record.mark_type,
                "createdAt": record.created_at
            }
        }, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500