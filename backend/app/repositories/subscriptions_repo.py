import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "subscriptions.json"

class SubscriptionsRepo:

    def load_subscriptions():
        with open(DATA_PATH, "r") as f:
            return json.load(f)
        
    def save_subscriptions(subs):
        with open(DATA_PATH, "w") as f:
            json.dump(subs, f, indent=4)

    def add_subscription(data):
        subs = SubscriptionsRepo.load_subscriptions()
        new_id = max([s["id"] for s in subs], default=0) + 1

        subscription = {
            "id": new_id,
            "user_id": data.user_id,
            "product_id": data.item_id,
            "interval_days": data.interval_days,
            "next_renewal": (datetime.now() + timedelta(days=data.interval_days)).isoformat(),
            "active": True
        }

        subs.append(subscription)
        SubscriptionsRepo.save_subscriptions(subs)

        return subscription
    
    def get_active_subscriptions():
        subs = SubscriptionsRepo.load_subscriptions()
        now = datetime.now()

        return [s for s in subs if s["activate"] and datetime.fromisoformat(s["next_renewal"]) <= now]
    
    def update_subscription(subscription):
        subs = SubscriptionsRepo.load()

        for i, s in enumerate(subs):
            if s["id"] == subscription["id"]:
                subs[i] = subscription
                break

        SubscriptionsRepo.save_subscriptions(subs)