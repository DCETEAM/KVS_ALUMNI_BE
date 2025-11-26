import qrcode
import os

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
