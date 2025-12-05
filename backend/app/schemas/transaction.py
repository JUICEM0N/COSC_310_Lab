from typing import Optional
from pydantic import BaseModel, field_validator
import datetime


class Transaction(BaseModel):
    transaction_id: str
    user_id: int
    amount: float
    currency: str = "cad"
    timestamp: datetime.datetime
    items: list[dict]
    status: str = "pending"
    payment_intent_id: Optional[str] = None
    refunded_at: Optional[datetime.datetime] = None

    @field_validator('currency')
    def validate_currency(cls, value):
        if value.lower() not in ['cad', 'usd', 'eur']:
            raise ValueError("Unsupported currency")
        return value.lower()

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    currency: str = "cad"
    items: list[dict]


class PaymentIntentRequest(BaseModel):
    currency: str = "cad"

    @field_validator('currency')
    def validate_currency(cls, value):
        if value.lower() not in ['cad', 'usd', 'eur']:
            raise ValueError("Unsupported currency")
        return value.lower()