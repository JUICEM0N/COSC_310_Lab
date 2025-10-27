from pydantic import BaseModel

class Cart(BaseModel):
    cart_id: int
    items: list[item]
    total_price: float

class CartCretae(BaseModel):
    items: list[item]
    total_price: float

class CartUpdate(BaseModel):
    items: list[item]
    total_price: float