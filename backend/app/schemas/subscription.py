from pydantic import BaseModel
from datetime import datetime

class Subscription(BaseModel):
    id: int
    user_id: str
    item_id: str
    interval_days: int
    next_renewal: datetime
    active: bool = True

class SubscriptionCreate(BaseModel):
    user_id: str
    item_id: str
    interval_days: int