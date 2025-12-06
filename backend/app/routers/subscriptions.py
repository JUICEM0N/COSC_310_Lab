from fastapi import APIRouter
from backend.app.schemas.subscription import SubscriptionCreate
from backend.app.repositories.subscriptions_repo import SubscriptionsRepo

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/create")
def create_subscripton(data: SubscriptionCreate):
    sub = SubscriptionsRepo.add_subscription(data)
    return {"message": "Subscription created", "subscription": sub}

@router.get("/{user_id}")
def list_user_subscriptions(user_id: int):
    subs = SubscriptionsRepo.load_subscriptions()
    return [s for s in subs if str(s["user_id"]) == str(user_id)]