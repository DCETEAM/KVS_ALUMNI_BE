import os
import random
from src.controllers.email_controller import send_enrollment_email
from src.controllers.qr_controller import generate_qr
from src.models.register_modal import Alumni
from src import db
from sqlalchemy import cast, String, func


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

def get_by_email(email):
    if not email:
        return None

    email = email.strip().lower()

    return Alumni.query.filter(
        func.lower(
            func.json_extract(Alumni.personal_basic, "$.email")
        ) == f'"{email}"'   # JSON_EXTRACT returns quoted string → must include quotes
    ).first()


def update_alumni(enroll_no, grouped_data, file=None):
    """
    Update an existing alumni record by enrollNumber.

    - Frontend sends a FLAT JSON (your Formik values).
    - We map that into the SAME JSON structure as existing DB rows, e.g.:

      personal_basic: {
          fullName, profileImage, standard, completedYear, batch, sportsHouse,
          countryCode, mobile, email, country, state, city, dob, occupation
      }

      personal_occupation: {
          specialization, institutionName, businessName, businessIndustry,
          businessRole, businessLocation, businessWebsite, businessDescription,
          companyName, companyRole, companyDepartment, companySector,
          companyLocation, companyLinkedin
      }

      event_participation: {...}
      sports_activity: {shuttle, tableTennis, tennis, cricket}
      business: {businessCollaboration, flyer}
      sponsorship: {sponsorType, sponsorEvent, sponsorBudget}
    """

    # Make sure enroll_no is string (column is String)
    enroll_no = str(enroll_no)

    # ----------------- FETCH RECORD -----------------
    alumni = Alumni.query.filter_by(enrollNumber=enroll_no).first()
    if not alumni:
        raise ValueError("Alumni not found")

    old_basic = alumni.personal_basic or {}

    # ----------------- PERSONAL BASIC -----------------
    personal_basic = {
        "fullName": grouped_data.get("fullName"),
        # keep old profileImage info if you were storing something here previously
        "profileImage": old_basic.get("profileImage"),  # typically null; actual file is profileAssetPath
        "standard": grouped_data.get("standard"),
        "completedYear": grouped_data.get("completedYear"),
        "batch": grouped_data.get("batch"),
        "sportsHouse": grouped_data.get("sportsHouse"),
        "countryCode": grouped_data.get("countryCode"),
        "mobile": grouped_data.get("mobile"),
        "email": grouped_data.get("email"),
        "country": grouped_data.get("country"),
        "state": grouped_data.get("state"),
        "city": grouped_data.get("city"),
        # DOB from frontend is already a string "YYYY-MM-DD" – store as-is in JSON
        "dob": grouped_data.get("dob"),
        "occupation": grouped_data.get("occupation"),
    }

    # ----------------- PERSONAL OCCUPATION -----------------
    personal_occupation = {
        "specialization": grouped_data.get("specialization"),
        "institutionName": grouped_data.get("institutionName"),
        "businessName": grouped_data.get("businessName"),
        "businessIndustry": grouped_data.get("businessIndustry"),
        "businessRole": grouped_data.get("businessRole"),
        "businessLocation": grouped_data.get("businessLocation"),
        "businessWebsite": grouped_data.get("businessWebsite"),
        "businessDescription": grouped_data.get("businessDescription"),
        "companyName": grouped_data.get("companyName"),
        "companyRole": grouped_data.get("companyRole"),
        "companyDepartment": grouped_data.get("companyDepartment"),
        "companySector": grouped_data.get("companySector"),
        "companyLocation": grouped_data.get("companyLocation"),
        "companyLinkedin": grouped_data.get("companyLinkedin"),
    }

    # ----------------- EVENT PARTICIPATION -----------------
    event_participation = {
        "eventConfirmation": grouped_data.get("eventConfirmation"),
        "foodPreference": grouped_data.get("foodPreference"),
        "volunteer": grouped_data.get("volunteer"),
        "marathon": grouped_data.get("marathon"),
        "groupDance": grouped_data.get("groupDance"),
        "playingSingingBand": grouped_data.get("playingSingingBand"),
        "instrument": grouped_data.get("instrument"),
        "singingType": grouped_data.get("singingType"),
    }

    # ----------------- SPORTS ACTIVITY -----------------
    # Frontend sends: sports: { shuttle, tableTennis, tennis, cricket }
    sports_activity = grouped_data.get("sports", {}) or {}

    # ----------------- BUSINESS (COLLABORATION) -----------------
    business = {
        "businessCollaboration": grouped_data.get("businessCollaboration"),
        "flyer": grouped_data.get("flyer"),
    }

    # ----------------- SPONSORSHIP -----------------
    sponsorship = {
        "sponsorType": grouped_data.get("sponsorType"),
        "sponsorEvent": grouped_data.get("sponsorEvent"),
        "sponsorBudget": grouped_data.get("sponsorBudget"),
    }

    # ----------------- DUPLICATE VALIDATION -----------------
    email = personal_basic.get("email")
    mobile = personal_basic.get("mobile")

    if email:
        exists_email = Alumni.query.filter(
            cast(Alumni.personal_basic["email"], String) == email,
            Alumni.enrollNumber != enroll_no
        ).first()
        if exists_email:
            raise ValueError("Email already exists")

    if mobile:
        exists_mobile = Alumni.query.filter(
            cast(Alumni.personal_basic["mobile"], String) == mobile,
            Alumni.enrollNumber != enroll_no
        ).first()
        if exists_mobile:
            raise ValueError("Mobile number already exists")

    # ----------------- FILE UPLOAD (PROFILE IMAGE) -----------------
    if file:
        full_name_clean = (personal_basic.get("fullName") or "user").replace(" ", "")
        ext = file.filename.split(".")[-1] if "." in file.filename else ""
        filename = f"{enroll_no}_{full_name_clean}.{ext}" if ext else f"{enroll_no}_{full_name_clean}"
        file_path = os.path.join(ASSET_FOLDER, filename)
        file.save(file_path)

        # delete previous image if exists and different
        old_filename = alumni.profileAssetPath
        if old_filename and old_filename != filename:
            old_path = os.path.join(ASSET_FOLDER, old_filename)
            if os.path.exists(old_path):
                os.remove(old_path)

        alumni.profileAssetPath = filename

    # ----------------- APPLY TO MODEL -----------------
    alumni.personal_basic = personal_basic
    alumni.personal_occupation = personal_occupation
    alumni.event_participation = event_participation
    alumni.sports_activity = sports_activity
    alumni.business = business
    alumni.sponsorship = sponsorship

    db.session.commit()
    return alumni
