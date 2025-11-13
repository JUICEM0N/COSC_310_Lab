from pydantic import BaseModel
import datetime

class Penalty(BaseModel):
    id: str
    user_id: int
    reason: str
    amount: float
    status: str
    date_issued: datetime.datetime

class PenaltyCreate(BaseModel):
    user_id: int
    reason: str
    amount: float
    status: str

class PenaltyUpdate(BaseModel):
    reason: str
    amount: float
    status: str