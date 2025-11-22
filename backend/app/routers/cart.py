from fastapi import APIRouter, HTTPException
from backend.app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/{user_id}")
def get_cart(user_id: int):
    return CartService.get_cart(user_id)

@router.post("/{user_id}/add")
def add_item(user_id:int, product_id: str, quantity: int = 1):
    CartService.add_item(user_id, product_id, quantity)
    return {"message": f"{product_id} added to cart {user_id}"}

@router.patch("/{user_id}/update")
def update_quantity(user_id: int, product_id: str, quantity: int):
    CartService.update_quantity(user_id, product_id, quantity)
    return {"message": "Quantity updated"}

@router.delete("/{user_id}/remove")
def remove_item(user_id: int, product_id: str):
    CartService.remove_item(user_id, product_id)
    return {"message": f"{product_id} removed from cart {user_id}"}

@router.delete("/{user_id}/clear")
def clear_cart(user_id: int):
    CartService.clear_cart(user_id)
    return {"message": f"Cleared cart for {user_id}"}