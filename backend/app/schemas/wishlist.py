from typing import List, Optional
from pydantic import BaseModel, Field

class WishlistItem(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")

class WishlistBase(BaseModel):
    user_id: int
    items: List[WishlistItem] = []
    public: bool = False
    shared_with: List[str] = []

class WishlistCreate(WishlistBase):
    user_id: int

class WishlistPrivacyUpdate(BaseModel):
    shared_with: Optional[List[str]] = None

class Wishlist(WishlistBase):
    user_id: int
    items: List[WishlistItem] = []

    class Config:
        orm_mode = True
