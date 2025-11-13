from typing import Dict, Optional
from schemas.cart import CartItem, Cart
from datetime import datetime

# In-memory storage for carts since we are not usign a DB
user_carts: Dict[str, Cart] = {}

def get_cart_by_user(user_id: str) -> Optional[Cart]:
    return user_carts.get(user_id)
