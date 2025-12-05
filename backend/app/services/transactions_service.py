from datetime import datetime, timedelta, date
import json
from backend.app.repositories.products_repo import ProductsRepo
from backend.app.repositories.cart_repo import CartRepo
from backend.app.repositories.transactions_repo import TransactionsRepo
from backend.app.services.email_service import EmailService
from backend.app.services.receipt_service import ReceiptService
from fastapi import HTTPException
import stripe


TAX_RATE = 0.12
EXCHANGE_RATES = {
    "cad": 1.0,
    "usd": 0.75,
    "eur": 0.68
}

def convert_amount(amount: float, target_currency: str) -> int:
    rate = EXCHANGE_RATES.get(target_currency.lower(), 1.0)
    converted = amount * rate
    return int(converted * 100)


def parse_price(price_str: str) -> float:
    if not price_str:
        return 0.0
    return float(price_str.replace("$", "").strip())

class TransactionsService:

    def get_cart_summary(user_id: int, currency = "cad"):
        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart for user '{user_id}' not found")

        cart = CartRepo.get_cart(user_id)
        items = []
        items_list = cart["items"]
        subtotal = 0.0

        for item in items_list:
            product_id = item["product_id"]
            quantity = item["quantity"]

            product = ProductsRepo.get_products(product_id)
            if not product:
                continue
            
            discounted_price = parse_price(product["discounted_price"])
            actual_price = parse_price(product["actual_price"])

            line_total = quantity * discounted_price
            subtotal += line_total

            items.append({
                "product_id": product_id,
                "name": product["product_name"],
                "quantity": quantity,
                "price_per_unit": discounted_price,
                "subtotal": line_total,
                "actual_price": actual_price,
                "discount": product.get("discount_percentage"),
                "category": product.get("category"),
                "rating": product.get("rating"),
                "rating_count": product.get("rating_count"),
                "image": product.get("img_link"),
            })

        tax = subtotal * TAX_RATE
        total = subtotal + tax

        return {
            "user_id": user_id,
            "items": items,
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "total": round(total, 2),
            "currency": currency.lower()
        }
    
    def create_payment_intent(user_id: int, currency: str = "cad"):
        summary = TransactionsService.get_cart_summary(user_id, currency)
        if not summary["items"]:
            raise HTTPException(400, "Empty cart")
        
        for item in summary["items"]:
            product = ProductsRepo.get_products(item["product_id"])
            if not product:
                raise HTTPException(400, f"Product {item['name']} is no longer available")
            
            available_stock = int(product.get("quantity", 0))
            if item["quantity"] > available_stock:
                raise HTTPException(400, f"Insufficient stock for {item['name']}. Only {available_stock} left.")

        transaction_data = {
            "user_id": user_id,
            "amount": summary["total"],
            "currency": currency,
            "items": summary["items"],
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
        saved_transaction = TransactionsRepo.add_transaction(transaction_data)
        transaction_id = saved_transaction["transaction_id"]

        amount_cents = convert_amount(summary["total"], currency)
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency.lower(),
            metadata={"transaction_id": transaction_id}
        )
        
        TransactionsRepo.update_transaction(transaction_id, {"payment_intent_id": intent["id"]})
        
        return intent
    
    @staticmethod
    def _finalize_order(transaction, intent):
        if transaction.get("status") == "completed":
            return

        user_id = transaction["user_id"]
        items = transaction["items"]
        
        order = {
            "user_id": user_id,
            "items": items,
            "subtotal": sum(item["subtotal"] for item in items),
            "tax": (intent["amount"] / 100) - sum(item["subtotal"] for item in items),
            "total": intent["amount"] / 100,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            email = ReceiptService.validate_user_email(user_id)
            receipt_hash = ReceiptService.generate_receipt_hash(order)
            html = ReceiptService.generate_html_receipt(order, receipt_hash)
            EmailService.send_email(
                to_email=email,
                subject="Your StackSquad Receipt - Payment Confirmed",
                html_body=html
            )
        except Exception as e:
            print(f"Failed to send receipt email: {e}")
        
        TransactionsRepo.update_transaction(transaction["transaction_id"], {
            "status": "completed",
            "payment_intent_id": intent["id"]
        })

        for item in items:
            ProductsRepo.update_stock(item["product_id"], -item["quantity"])
        CartRepo.clear_cart(user_id)

    def fulfill_transaction(event: dict):
        if event["type"] != "payment_intent.succeeded":
            return
        intent = event["data"]["object"]
        
        transaction_id = intent["metadata"].get("transaction_id")
        transaction = None
        
        if transaction_id:
            transaction = TransactionsRepo.get_transaction_by_id(transaction_id)
        
        if not transaction:
            transaction = TransactionsRepo.get_transaction_by_intent(intent["id"])
            
        if not transaction:
            print(f"Transaction not found for intent {intent['id']}")
            return
            
        TransactionsService._finalize_order(transaction, intent)

    def confirm_payment(payment_intent_id: str):
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if intent["status"] != "succeeded":
            raise HTTPException(400, f"Payment not succeeded. Status: {intent['status']}")
            
        transaction = TransactionsRepo.get_transaction_by_intent(payment_intent_id)
        if not transaction:
            transaction_id = intent["metadata"].get("transaction_id")
            if transaction_id:
                transaction = TransactionsRepo.get_transaction_by_id(transaction_id)
        
        if not transaction:
            raise HTTPException(404, "Transaction not found for this payment")
            
        TransactionsService._finalize_order(transaction, intent)
        return {"status": "success", "transaction_id": transaction["transaction_id"]}

    def process_refund(transaction_id: str):
        transaction = TransactionsRepo.get_transaction_by_id(transaction_id)
        if not transaction:
            raise HTTPException(404, "Transaction not found")
        transaction_time = datetime.fromisoformat(transaction["timestamp"])
        if datetime.now() - transaction_time > timedelta(days=14):
            raise HTTPException(403, "Refund period has expired")
        refund = stripe.Refund.create(
            payment_intent = transaction["payment_intent_id"],
            amount = int(transaction["amount"] * 100)
        )
        if refund["status"] == "succeeded":
            TransactionsRepo.update_transaction(transaction_id, {
                "status": "refunded",
                "refunded_at": datetime.now()
            })
            for item in transaction["items"]:
                ProductsRepo.update_stock(item["product_id"], item["quantity"])
        return refund
         
    #fallback for checkout without stripe
    def checkout(user_id: int):
        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart for user '{user_id}' not found")
        
        cart = CartRepo.get_cart(user_id)

        if len(cart["items"]) == 0:
            raise HTTPException(status_code=400, detail="Cannot checkout an empty cart")

        email = ReceiptService.validate_user_email(user_id)

        order = ReceiptService.build_order(user_id)

        receipt_hash = ReceiptService.generate_receipt_hash(order)

        html = ReceiptService.generate_html_receipt(order, receipt_hash)

        EmailService.send_email(
            to_email=email,
            subject="Your StackSquad Receipt",
            html_body=html
        )

        transaction = {
            "id": receipt_hash,
            "user_id": user_id,
            "date": str(date.today()),
            "status": "completed",
            "products": order["items"],
            "subtotal": order["subtotal"],
            "tax": order["tax"],
            "total_amount": order["total"],
        }

        TransactionsRepo.add_transaction(transaction)
        CartRepo.clear_cart(user_id)

        return {
            "message": "Checkout complete — receipt emailed.",
            "receipt_id": receipt_hash,
            "total": order["total"],
            "items": order["items"]
        }