from pydantic import BaseModel
import datetime

class Transaction(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    timestamp: datetime.datetime

class TransactionCreate(BaseModel):
    user_id: int
    amount: float