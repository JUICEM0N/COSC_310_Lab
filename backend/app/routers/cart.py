from fastapi import APIRouter, HTTPException

# Uncomment below when testing with PyTest
# from backend.app.schemas.cart import CartItem, Cart
# from backend.app.services.cart_service import get_cart_by_user, get_cart_items, add_cart_item, update_cart_item, remove_cart_item

# Uncomment below when running FastAPI
from schemas.cart import CartItem, Cart
from services.cart_service import get_cart_by_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/{user_id}", response_model=Cart)
def get_user_cart(user_id: str):
    cart = get_cart_by_user(user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart