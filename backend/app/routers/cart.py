from fastapi import APIRouter, HTTPException

# Uncomment below when testing with PyTest
# from backend.app.schemas.cart import CartItem, Cart
# from backend.app.services.cart_service import get_cart_by_user, get_cart_items, add_cart_item, update_cart_item, remove_cart_item

# Uncomment below when running FastAPI
from repositories.cart_repo import CartRepo

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/{user_id}")
def get_cart(user_id: int):
    return CartRepo.get_cart(user_id)

@router.post("/{user_id}/add")
def add_item(user_id:int, product_id: str, quantity: int = 1):
    CartRepo.add_item(user_id, product_id, quantity)
    return {"message": f"{product_id} added to cart {user_id}"}

@router.patch("/{user_id}/update")
def update_quantity(user_id: int, product_id: str, quantity: int):
    CartRepo.update_quantity(user_id, product_id, quantity)
    return {"message": "Quantity updated"}

@router.delete("/{user_id}/remove")
def remove_item(user_id: int, product_id: str):
    CartRepo.remove_item(user_id, product_id)
    return {"message": f"{product_id} removed from cart {user_id}"}

@router.delete("/{user_id}/clear")
def clear_cart(user_id: int):
    CartRepo.clear_cart(user_id)
    return {"message": f"Cleared cart for {user_id}"}