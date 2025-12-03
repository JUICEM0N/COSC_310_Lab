import os
import requests
import time

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_REPLY_TO = os.getenv("EMAIL_REPLY_TO")

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

class EmailService:

    def send_email(to_email: str, subject: str, html_body: str, retries=3):
        headers = {
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "personalizations": [{
                "to": [{"email": to_email}]
            }],
            "from": {"email": EMAIL_FROM},
            "reply_to": {"email": EMAIL_REPLY_TO},
            "subject": subject,
            "content": [{
                "type": "text/html",
                "value": html_body
            }]
        }

        for _ in range(retries):
            response = requests.post(SENDGRID_URL, headers=headers, json=payload)

            if response.status_code in (200, 202):
                return True

            time.sleep(1)

        raise RuntimeError(f"Email failed after {retries} attempts: {response.text}")
