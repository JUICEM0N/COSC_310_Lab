from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    product_id: str
    product_name: str
    category: str
    discounted_price: Optional[str] = None
    actual_price: str
    discount_percentage: Optional[str] = None
    rating: str
    rating_count: str
    about_product: str
    user_id: str
    user_name: str
    review_id: str
    review_title: str
    review_content: str
    img_link: str
    product_link: str
    quantity: int

class ItemCreate(BaseModel):
    product_id: str
    product_name: str
    category: str
    discounted_price: str
    actual_price: str
    discount_percentage: str
    rating: str
    rating_count: str
    about_product: str
    user_id: str
    user_name: str
    review_id: str
    review_title: str
    review_content: str
    img_link: str
    product_link: str
    quantity: int

class ItemUpdate(BaseModel):
    product_name: str
    category: str
    discounted_price: str
    actual_price: str
    discount_percentage: str
    rating: str
    rating_count: str
    about_product: str
    user_id: str
    user_name: str
    review_id: str
    review_title: str
    review_content: str
    img_link: str
    product_link: str
    quantity: int