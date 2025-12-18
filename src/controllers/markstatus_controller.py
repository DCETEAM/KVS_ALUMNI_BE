from src import db
from src.models.markstatus_modal import MarkStatus
from src.models.register_modal import Alumni
from sqlalchemy import func

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
    
def get_mark_status(enroll_no):
    try:
        # Fetch ALL marks for the user
        records = MarkStatus.query.filter_by(enrollNumber=enroll_no).all()

        status_map = {
            "Entry": False,
            "Food": False,
            "Kit Bag": False
        }

        # Map db records → UI
        for r in records:
            if r.markType in status_map:
                status_map[r.markType] = True

        return {
            "status": "success",
            "data": status_map
        }, 200

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

def get_marktype_counts():
    """
    Returns total counts of Entry / Food / Kit Bag
    """

    results = (
        db.session.query(
            MarkStatus.markType,
            func.count(MarkStatus.id)
        )
        .group_by(MarkStatus.markType)
        .all()
    )

    # Default response
    data = {
        "Entry": 0,
        "Food": 0,
        "Kit Bag": 0
    }

    for mark_type, count in results:
        if mark_type in data:
            data[mark_type] = count

    return {
        "status": "success",
        "data": data
    }, 200

def get_marktype_details(mark_type, page=1, per_page=10, search=None):
    try:
        query = (
            db.session.query(
                MarkStatus.id,
                MarkStatus.enrollNumber,
                MarkStatus.timestamp,
                Alumni.personal_basic
            )
            .join(Alumni, Alumni.enrollNumber == MarkStatus.enrollNumber)
            .filter(MarkStatus.markType == mark_type)
            .order_by(MarkStatus.timestamp.desc())
        )

        if search:
            search = f"%{search}%"
            query = query.filter(
                func.JSON_EXTRACT(Alumni.personal_basic, "$.fullName").like(search) |
                func.JSON_EXTRACT(Alumni.personal_basic, "$.mobile").like(search) |
                MarkStatus.enrollNumber.like(search)
            )

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        rows = []
        for idx, r in enumerate(pagination.items, start=1 + (page - 1) * per_page):
            rows.append({
                "sno": idx,
                "enrollNumber": r.enrollNumber,
                "fullName": r.personal_basic.get("fullName"),
                "mobile": r.personal_basic.get("mobile"),
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })

        return {
            "status": "success",
            "data": rows,
            "total": pagination.total,
            "page": page,
            "perPage": per_page
        }, 200

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500