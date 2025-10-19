from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: str
    product_name: str
    product_category: str
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

class ItemCreate(BaseModel):
    product_name: str
    product_category: str
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

class ItemUpdate(BaseModel):
    product_name: str
    product_category: str
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
