import os
import requests
from flask import current_app


def send_whatsapp_with_qr(
    phone: str,
    message: str,
    qr_filename: str
):
    """
    Send WhatsApp text message with an existing QR PNG attachment
    QR path: src/assets/qrcodes/<qr_filename>
    """

    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCIgOiAiYTRiMjM0MGMtZGE0ZC00YWVkLTgyY2MtYTJlMGI2ZDU3ZWU3IiwgInJvbGUiIDogImFwaSIsICJ0eXBlIiA6ICJhcGkiLCAibmFtZSIgOiAiS1ZTLVRFU1QiLCAiZXhwIiA6IDIwODEzMTc2MTMsICJpYXQiIDogMTc2NTc4NDgxMywgInN1YiIgOiAiNDAxYTVmNzItZDJhOS00MWYxLTkxMTItNDE2YTA2YzVjNjEyIiwgImlzcyIgOiAicGVyaXNrb3BlLmFwcCIsICJtZXRhZGF0YSIgOiB7InNjb3BlcyI6IFsiOTE4MDE1ODc3OTIxQGMudXMiXX19.Rdmor-1cstlupW2JCyKD-V4oJxDO0zEarFB3Id6Scj4"
    TEXT_URL = "https://api.periskope.app/v1/message/send"
    MEDIA_URL = "https://api.periskope.app/v1/message/send"

    # ---------- Send Text Message ----------
    headers_text = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}",
        "x-phone": "918015877921"
    }

    text_payload = {
        "chat_id": f"91{phone}@c.us",
        "message": message
    }

    requests.post(TEXT_URL, json=text_payload, headers=headers_text)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}",
        "x-phone": "918015877921"
    }

    payload = {
        "chat_id": f"91{phone}@c.us",
        "media": {
                "type": "image",
                "filename": qr_filename,
                "mimetype": "image/png",
                "url": f"https://dceconnect.in/kvs-api/register/profile/qr/{qr_filename}"
            }
    }

    requests.post(
        "https://api.periskope.app/v1/message/send",
        headers=headers,
        json=payload
    )
