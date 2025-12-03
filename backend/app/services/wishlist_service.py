from backend.app.repositories.wishlist_repo import WishlistRepo
from backend.app.repositories.products_repo import ProductsRepo
from backend.app.repositories.users_repo import UsersRepo
from fastapi import HTTPException
from typing import List, Optional

class WishlistService:

    @staticmethod
    def create_wishlist(user_id: int, public: bool = False):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")
        if WishlistRepo.wishlist_exists(user_id):
            raise HTTPException(status_code=400, detail=f"Wishlist already exists for user {user_id}")
        return WishlistRepo.create_wishlist(user_id, public)

    @staticmethod
    def get_wishlist(user_id: int):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"User does not exist: {user_id}")
        wishlist = WishlistRepo.get_wishlist(user_id)
        if not wishlist:
            raise HTTPException(status_code=404, detail=f"Wishlist does not exist for user: {user_id}")
        return wishlist

    @staticmethod
    def add_item(user_id: int, product_id: str, quantity: int = 1):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        if not ProductsRepo.product_exists(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        if not WishlistRepo.wishlist_exists(user_id):
            WishlistRepo.create_wishlist(user_id, public=False)
        WishlistRepo.add_item(user_id, product_id, quantity)

    @staticmethod
    def remove_item(user_id: int, product_id: str):
        wishlist = WishlistRepo.get_wishlist(user_id)
        if not wishlist:
            raise HTTPException(status_code=404, detail=f"Wishlist does not exist for user: {user_id}")
        wishlist["items"] = [i for i in wishlist["items"] if i["product_id"] != product_id]
        WishlistRepo.update_wishlist(user_id, wishlist)

    @staticmethod
    def clear_wishlist(user_id: int):
        wishlist = WishlistRepo.get_wishlist(user_id)
        if not wishlist:
            raise HTTPException(status_code=404, detail=f"Wishlist does not exist for user: {user_id}")
        wishlist["items"] = []
        WishlistRepo.update_wishlist(user_id, wishlist)

    def update_privacy(user_id: int, public: bool = None, shared_with: list[str] = None):
        wishlist = WishlistRepo.get_wishlist(user_id)
        if not wishlist:
            raise HTTPException(status_code=404, detail="Wishlist not found")

        if public is not None:
            wishlist["public"] = public
        if shared_with is not None:
            wishlist["shared_with"] = shared_with

        WishlistRepo.update_wishlist(user_id, wishlist)