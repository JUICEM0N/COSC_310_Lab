from pathlib import Path
import json
from fastapi import HTTPException

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
        return next((c for c in carts if c.get("user_id") == user_id), None)


    @staticmethod
    def update_cart(user_id: int, items):
        carts = CartRepo.load_carts()
        
        for cart in carts:
            if cart.get("user_id") == user_id:
                cart["items"] = items
                CartRepo.save_carts(carts)
                return

        raise HTTPException(status_code=404, detail="Cart not found")

    @staticmethod
    def add_item(user_id: int, product_id: str, quantity: int = 1):
        cart = CartRepo.get_cart(user_id)

        if cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")

        items = cart["items"]

        existing = next((i for i in items if i.get("product_id") == product_id), None)

        if existing:
            existing["quantity"] += quantity
        else:
            items.append({"product_id": product_id, "quantity": quantity})

        CartRepo.update_cart(user_id, items)

    @staticmethod
    def remove_item(user_id: int, product_id: str):
        cart = CartRepo.get_cart(user_id)
        
        if cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")

        items = cart["items"]
        new_items = [i for i in items if i.get("product_id") != product_id]

        CartRepo.update_cart(user_id, new_items)

    @staticmethod
    def clear_cart(user_id: int):
        CartRepo.update_cart(user_id, [])

    @staticmethod
    def update_quantity(user_id: int, product_id: str, quantity: int):
        cart = CartRepo.get_cart(user_id)

        items = cart["items"]

        found = False

        for item in items:
            if item.get("product_id") == product_id:
                found = True
                if quantity <= 0:
                    items.remove(item)
                else:
                    item["quantity"] = quantity
                break
                
        if not found:
            raise HTTPException(status_code=404, detail="Item not found in cart")
        
        CartRepo.update_cart(user_id, items)

    def cart_exists(user_id: int) -> bool:
        carts = CartRepo.load_carts()
        return any(c.get("user_id") == user_id for c in carts)
    
    def item_in_cart(user_id: int, product_id: str) -> bool:
        cart = CartRepo.get_cart(user_id)
        items = cart["items"]
        
        return any(i.get("product_id") == product_id for i in items)
    
    def create_cart_for_user(user_id: int):
        carts = CartRepo.load_carts()

        if any(c.get("user_id") == user_id for c in carts):
            return

        new_cart = {
            "user_id": user_id,
            "items": []
        }

        carts.append(new_cart)
        CartRepo.save_carts(carts)
