from pydantic import BaseModel

class CartItem(BaseModel):
    product_id: str
    namme: str
    quantity: int
    price_per_unit: float
    total_price: float

class Cart(BaseModel):
    cart_id: int
    items: list[CartItem]
    total_price: float

# Delete below, same thing as Cart?
class CartCreate(BaseModel):
    items: list[CartItem]
    total_price: float

class CartUpdate(BaseModel):
    items: list[CartItem]
    total_price: float