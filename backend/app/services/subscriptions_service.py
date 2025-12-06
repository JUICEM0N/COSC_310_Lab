from backend.app.repositories.subscriptions_repo import SubscriptionsRepo
from backend.app.repositories.transactions_repo import TransactionsRepo
from backend.app.repositories.products_repo import ProductsRepo
from backend.app.services.items_service import ItemsService
from datetime import datetime, timedelta

def process_subscriptions():
    subs = SubscriptionsRepo.get_active_subscriptions()

    for s in subs:
        product = ProductsRepo.get_product_by_id(s["product_id"])
        
        if not product:
            continue

        item_entry = ItemsService.build_transaction_item(product, quantity=1)

        transaction = {
            "user_id": s["user_id"],
            "amount": item_entry["subtotal"],
            "currency": "CAD", 
            "items": [item_entry],
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
        
        TransactionsRepo.add_transaction(transaction)

        next_date = datetime.now() + timedelta(days=s["interval_days"])
        s["next_renewal"] = next_date.isoformat()
        SubscriptionsRepo.update_subscription(s)