import qrcode
import os
from flask import request, jsonify
from src.utils.whatsapp_service import send_whatsapp_with_qr

QR_FOLDER = "src/assets/qrcodes"
os.makedirs(QR_FOLDER, exist_ok=True)

def generate_qr(enroll_no):
    # QR will contain ONLY the enrollment number
    qr_data = enroll_no  
    
    filename = f"{enroll_no}.png"
    qr_path = os.path.join(QR_FOLDER, filename)

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    return qr_path



def send_alumni_qr_controller():
    data = request.get_json()

    phone = data.get("phone")
    qr_filename = data.get("qr_filename")

    if not phone or not qr_filename:
        return jsonify({
            "success": False,
            "message": "phone and qr_filename are required"
        }), 400

    message = (
        "🎉 *KVS Soolakarai Alumni Meet - Registration Confirmed!* 🎉\n\n"
        "Please find your QR code attached.\n\n"
        "Use this QR for:\n"
        "✅ Entry\n"
        "🍽️ Food\n"
        "🎒 Kid Bag\n\n"
        "Alumni Meet Committee"
    )

    send_whatsapp_with_qr(
        phone=phone,
        message=message,
        qr_filename=qr_filename
    )

    return jsonify({
        "success": True,
        "message": "WhatsApp QR sent successfully"
    })

