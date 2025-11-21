from pathlib import Path
import json

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cart.json"

class CartRepo:
    @staticmethod
    def load_carts():
        if not DATA_PATH.exists():
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump([], f)
            return []

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        
        return data if isinstance(data, list) else []

    @staticmethod
    def save_carts(carts):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(carts, f, indent=4)

    @staticmethod
    def get_cart(user_id: int):
        carts = CartRepo.load_carts()

        cart = next((c for c in carts if c.get("user_id") == user_id), None)

        if cart is None:
            cart = {"user_id": user_id, "items": []}
            carts.append(cart)
            CartRepo.save_carts(carts)

        return cart["items"]

    @staticmethod
    def update_cart(user_id: int, items):
        carts = CartRepo.load_carts()
        found = False

        for cart in carts:
            if cart.get("user_id") == user_id:
                cart["items"] = items
                found = True
                break

        if not found:
            carts.append({"user_id": user_id, "items": items})

        CartRepo.save_carts(carts)

    @staticmethod
    def add_item(user_id: int, product_id: str, quantity: int = 1):
        items = CartRepo.get_cart(user_id)

        existing = next((i for i in items if i.get("product_id") == product_id), None)

        if existing:
            existing["quantity"] += quantity
        else:
            items.append({
                "product_id": product_id,
                "quantity": quantity
            })

        CartRepo.update_cart(user_id, items)

    @staticmethod
    def remove_item(user_id: int, product_id: str):
        items = CartRepo.get_cart(user_id)
        items = [i for i in items if i.get("product_id") != product_id]
        CartRepo.update_cart(user_id, items)

    @staticmethod
    def clear_cart(user_id: int):
        CartRepo.update_cart(user_id, [])

    @staticmethod
    def update_quantity(user_id: int, product_id: str, quantity: int):
        items = CartRepo.get_cart(user_id)

        for item in items:
            if item.get("product_id") == product_id:
                if quantity <= 0:
                    items.remove(item)
                else:
                    item["quantity"] = quantity
                break

        CartRepo.update_cart(user_id, items)