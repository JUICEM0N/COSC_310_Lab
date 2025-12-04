from typing import Dict, Any
from pathlib import Path
import json
import os

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "wishlists.json"

class WishlistRepo:

    @staticmethod
    def _ensure_file():
        if not DATA_PATH.exists():
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    @staticmethod
    def load_all() -> list:
        WishlistRepo._ensure_file()
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_all(wishlists: list):
        tmp = DATA_PATH.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(wishlists, f, indent=2)
        os.replace(tmp, DATA_PATH)

    @staticmethod
    def wishlist_exists(user_id: int) -> bool:
        return any(w["user_id"] == user_id for w in WishlistRepo.load_all())

    @staticmethod
    def create_wishlist(user_id: int, public: bool = False) -> Dict[str, Any]:
        wishlists = WishlistRepo.load_all()
        
        if any(w.get("user_id") == user_id for w in wishlists):
            return
        
        wishlist = {
            "user_id": user_id,
            "items": [],
            "public": public,
            "shared_with": []
        }
        wishlists.append(wishlist)
        WishlistRepo.save_all(wishlists)
        return wishlist

    @staticmethod
    def get_wishlist(user_id: int) -> Dict[str, Any] | None:
        return next((w for w in WishlistRepo.load_all() if w["user_id"] == user_id), None)

    @staticmethod
    def add_item(user_id: int, product_id: str, quantity: int):
        wishlists = WishlistRepo.load_all()
        for w in wishlists:
            if w["user_id"] == user_id:
                # Check if item already exists
                existing = next((i for i in w["items"] if i["product_id"] == product_id), None)
                if existing:
                    existing["quantity"] += quantity
                else:
                    w["items"].append({"product_id": product_id, "quantity": quantity})
                break
        WishlistRepo.save_all(wishlists)

    @staticmethod
    def update_wishlist(user_id: int, wishlist_data: dict):
        wishlists = WishlistRepo.load_all()
        for i, w in enumerate(wishlists):
            if w["user_id"] == user_id:
                wishlists[i] = wishlist_data
                break
        WishlistRepo.save_all(wishlists)
