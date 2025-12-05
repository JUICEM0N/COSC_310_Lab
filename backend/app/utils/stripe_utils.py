import stripe
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import HTTPException

env_path = Path(__file__).resolve().parent.parent / "totally_not_private_keys.env"
load_dotenv(dotenv_path=env_path)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

if not stripe.api_key:
    raise RuntimeError("STRIPE_SECRET_KEY not found in environment. Check totally_not_private_keys.env")

def verify_webhook(payload: bytes, sig_header: str):
    try:
        return stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")