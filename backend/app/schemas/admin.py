from pydantic import BaseModel

class PromoteUser(BaseModel):
    user_id: int


class ApplyPenalty(BaseModel):
    user_id: int
    reason: str
    amount: float
    status: str