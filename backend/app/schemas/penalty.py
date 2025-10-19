from pydantic import BaseModel
import datetime

class Penalty(BaseModel):
    id: str
    user_id: int
    reason: str
    amount: float
    date_issued: datetime.datetime

class PenaltyCreate(BaseModel):
    user_id: int
    reason: str
    amount: float

class PenaltyUpdate(BaseModel):
    reason: str
    amount: float