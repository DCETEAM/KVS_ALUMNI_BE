import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders


# Updated SMTP Config (GoDaddy / secureserver.net)
SMTP_CONFIG = {
    "host": "mail.dceconnect.in",
    "port": 465,
    "username": "support@dceconnect.in",
    "password": "Support@2025",
    "from_email": "support@dceconnect.in",
    "sender_name": "KVS Soolakkarai Alumni Association"
}

def send_enrollment_email(
    to_email,
    full_name,
    enroll_no,
    qr_path=None,
    attachment_ids=None,
    addons_file_paths=None,
    logo_path="src/assets/logo.png",
    cc_email_sent=False
):

    if not to_email:
        return {"error": "Email address not provided"}

    try:
        print("Preparing email...")

        # MIMEMultipart (related) enables inline images
        msg = MIMEMultipart("related")
        msg["From"] = f"{SMTP_CONFIG['sender_name']} <{SMTP_CONFIG['from_email']}>"
        msg["To"] = to_email
        msg["Subject"] = "Registration Confirmed - KVS Soolakkarai Alumni Meet"


        # Alternative part for HTML
        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)

        # Email HTML template
        html = f"""
<html>
<body style="font-family:Arial; background:#f5f7fa; padding:20px;">
    <div style="max-width:600px; margin:auto; background:white; padding:25px; border-radius:10px; box-shadow:0 0 10px #ddd;">

        <h2 style="text-align:center; color:#1e3a8a;">KVS Soolakkarai Alumni Meet 2025</h2>

        <p>Dear <strong>{full_name}</strong>,</p>

        <p>
            Thank you for registering for the 
            <strong>4th KVS Soolakkarai Alumni Meet</strong>.<br>
            Your registration has been successfully received.
        </p>

        <div style="border-left:4px solid #1e3a8a; 
                    background:#eef3ff; 
                    padding:10px 15px; 
                    margin:20px 0;">
            <h3 style="margin-top:0;">Event Details</h3>

            <p>📅 <strong>Date:</strong> 28 Dec 2025</p>
            <p>⏰ <strong>Time:</strong> 07:00 AM – 02:00 PM</p>
            <p>📍 <strong>Venue:</strong> Kshatriya Vidyasala English Medium School, Virudhunagar</p>
        </div>

        <p>
            We look forward to welcoming you and reconnecting with fellow alumni across all batches. <br>
            Further event updates and instructions will be shared with you soon.
        </p>

        <p>
            If you have any questions, feel free to reach out: 
            <a href="mailto:kvssoolakkaraiobavnr@gmail.com">kvssoolakkaraiobavnr@gmail.com</a>
        </p>

        <p>
            Warm regards,<br>
            <strong>KVS Soolakkarai Alumni Association</strong>
        </p>

        <br>
        <img src="cid:logo_image" style="width:120px; opacity:0.9;">
    </div>
</body>
</html>
"""

        msg_alt.attach(MIMEText(html, "html"))

        # Attach QR Code
        if qr_path and os.path.exists(qr_path):
            with open(qr_path, "rb") as f:
                mime = MIMEBase("image", "png")
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                mime.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(qr_path)}"'
                )
                msg.attach(mime)
            print("QR Code attached")

        # DB Attachment IDs
        
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
            server.login(SMTP_CONFIG["username"], SMTP_CONFIG["password"])
            server.sendmail(
                SMTP_CONFIG["from_email"],
                [to_email],
                msg.as_string()
            )

        print("Email sent successfully!")
        return {"success": True, "message": "Email sent successfully"}

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        return {"error": str(e)}


def send_enroll_number_email(to_email):
    # get the record of the alumni with given email
    from src.controllers.register_controller import get_by_email    
    alumni = get_by_email(to_email)
    print("Alumni fetched for enroll number email:", alumni)
    if not alumni:
        return {
            "success": False,
            "message": "No alumni found with the provided email."
        }, 400
    enroll_no = alumni.enrollNumber
    full_name = alumni.personal_basic.get("fullName", "Alumni") 
    try:
        print("Preparing enrollment number email...")

        # MIMEMultipart
        msg = MIMEMultipart()
        msg["From"] = f"{SMTP_CONFIG['sender_name']} <{SMTP_CONFIG['from_email']}>"
        msg["To"] = to_email
        msg["Subject"] = "Your Enrollment Number - KVS Soolakkarai Alumni Meet"

        # Email HTML template
        html = f"""
<html>
<body style="font-family:Arial; background:#f5f7fa; padding:20px;">
    <div style="max-width:600px; margin:auto; background:white; padding:25px; border-radius:10px; box-shadow:0 0 10px #ddd;">

        <h2 style="text-align:center; color:#1e3a8a;">KVS Soolakkarai Alumni Meet 2025</h2>

        <p>Dear <strong>{full_name}</strong>,</p>

        <p>
            As per your request, here is your enrollment number for the 
            <strong>4th KVS Soolakkarai Alumni Meet</strong>:
        </p>

        <div style="border-left:4px solid #1e3a8a; 
                    background:#eef3ff; 
                    padding:10px 15px; 
                    margin:20px 0;">
            <h3 style="margin-top:0;">Your Enrollment Number</h3>

            <p style="font-size:18px;"><strong>{enroll_no}</strong></p>
        </div>

        <p>
            Please keep this enrollment number safe as it will be required for event registration and participation.
        </p>

        <p>
            If you have any questions, feel free to reach out: 
            <a href="mailto:kvssoolakkaraiobavnr@gmail.com">kvssoolakkaraiobavnr@gmail.com</a>
        </p>
        <p>
            Warm regards,<br>
            <strong>KVS Soolakkarai Alumni Association</strong>
        </p>
    </div>
</body>
</html>
"""
        msg.attach(MIMEText(html, "html"))

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
            server.login(SMTP_CONFIG["username"], SMTP_CONFIG["password"])
            server.sendmail(
                SMTP_CONFIG["from_email"],
                [to_email],
                msg.as_string()
            )

        print("Enrollment number email sent successfully!")
        return {
            "success": True,
            "message": "Enrollment number email sent successfully",
            "enrollNumber": enroll_no
        }, 200
    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        return {
            "success": False,
            "message": str(e)
        }, 500
    