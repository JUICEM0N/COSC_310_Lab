from datetime import date
from backend.app.repositories.products_repo import ProductsRepo
from backend.app.repositories.cart_repo import CartRepo
from backend.app.repositories.transactions_repo import TransactionsRepo
from fastapi import HTTPException

TAX_RATE = 0.12

def parse_price(price_str: str) -> float:
    if not price_str:
        return 0.0
    return float(price_str.replace("$", "").strip())

class TransactionsService:

    def get_cart_summary(user_id: int):
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
            "total": round(total, 2)
        }
    
    def checkout(user_id: int):
        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart for user '{user_id}' not found")
        
        cart = CartRepo.get_cart(user_id)

        if len(cart["items"]) == 0:
            raise HTTPException(status_code=400, detail="Cannot checkout an empty cart")

        summary = TransactionsService.get_cart_summary(user_id)

        receipt = {
            # "transaction_id": "str(uuid.uuid4())",
            "user_id": user_id,
            "products": summary["items"],
            "total_amount": summary["total"],
            "date": str(date.today()),
            "status": "completed"
        }

        TransactionsRepo.add_transaction(receipt)
        CartRepo.clear_cart(user_id)

        return receipt