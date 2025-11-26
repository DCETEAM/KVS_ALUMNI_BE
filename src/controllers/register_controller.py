import os
import random
from src.controllers.email_controller import send_enrollment_email
from src.controllers.qr_controller import generate_qr
from src.models.register_modal import Alumni
from src import db

ASSET_FOLDER = os.path.join(os.getcwd(), "src", "assets")
os.makedirs(ASSET_FOLDER, exist_ok=True)

def generate_enroll_no():
    """Generate unique 6-digit number"""
    while True:
        number = str(random.randint(100000, 999999))
        exists = Alumni.query.filter_by(enrollNumber=number).first()
        if not exists:
            return number


def create_alumni(grouped_data, file):
    personal_basic = grouped_data.get("personalDetails", {}).get("basic", {})
    occupation_details = grouped_data.get("personalDetails", {}).get("occupationDetails", {})
    event_participation = grouped_data.get("eventParticipation", {})
    sports_activity = grouped_data.get("sportsActivity", {})
    business = grouped_data.get("business", {})
    sponsorship = grouped_data.get("sponsorship", {})

    # --------------------------------
    # Duplicate Validation
    # --------------------------------
    from sqlalchemy import cast, String

    email = personal_basic.get("email")
    mobile = personal_basic.get("mobile")

    exists_email = Alumni.query.filter(
        cast(Alumni.personal_basic["email"], String) == email
    ).first()

    if exists_email:
        raise ValueError("Email already exists")

    exists_mobile = Alumni.query.filter(
        cast(Alumni.personal_basic["mobile"], String) == mobile
    ).first()

    if exists_mobile:
        raise ValueError("Mobile number already exists")


    # Enrollment Number
    enroll_no = generate_enroll_no()

    # File Upload
    filename = None
    if file:
        full_name_clean = personal_basic.get("fullName", "user").replace(" ", "")
        ext = file.filename.split(".")[-1]
        filename = f"{enroll_no}_{full_name_clean}.{ext}"
        file_path = os.path.join(ASSET_FOLDER, filename)
        file.save(file_path)

    # Create DB record
    alumni = Alumni(
        enrollNumber=enroll_no,
        profileAssetPath=filename,

        personal_basic=personal_basic,
        personal_occupation=occupation_details,

        event_participation=event_participation,
        sports_activity=sports_activity,
        business=business,
        sponsorship=sponsorship
    )

    db.session.add(alumni)
    db.session.commit()

    # QR Generation
    qr_path = generate_qr(enroll_no)

    # Email Notification
    send_enrollment_email(
        to_email=email,
        full_name=personal_basic.get("fullName"),
        enroll_no=enroll_no,
        qr_path=qr_path
    )

    return alumni



def get_all():
    return Alumni.query.all()


def get_by_id(alumni_id):
    return Alumni.query.get(alumni_id)

def get_by_enroll_number(enroll_no):
    return Alumni.query.filter_by(enrollNumber=enroll_no).first()

