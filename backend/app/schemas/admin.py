from pydantic import BaseModel
from typing import List

class PromoteUser(BaseModel):
    user_id: int

class ApplyPenalty(BaseModel):
    user_id: int
    reason: str
    amount: float
    status: str
class Admin(BaseModel):
    admin_id: int
    username: str
    password: str

class ProductOfWeekSelection(BaseModel):
    product_ids: List[int]

class ApplyDiscount(BaseModel):
    product_id: int
    discount_percent: float
