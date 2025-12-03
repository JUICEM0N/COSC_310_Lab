import pytest
from pydantic import ValidationError
from backend.app.schemas.wishlist import WishlistCreate, WishlistPrivacyUpdate

def test_wishlist_create_valid():
    data = {"user_id": 1, "items": [{"product_id": "123", "quantity": 2}]}
    wishlist = WishlistCreate(**data)
    assert wishlist.user_id == 1
    assert wishlist.items[0].product_id == "123"
    assert wishlist.items[0].quantity == 2

def test_wishlist_create_invalid():
    data = {"user_id": "abc", "items": "notalist"}
    with pytest.raises(ValidationError):
        WishlistCreate(**data)

def test_wishlist_privacy_update_valid():
    data = {"shared_with": ["alice", "bob"]}
    privacy = WishlistPrivacyUpdate(**data)
    assert privacy.shared_with == ["alice", "bob"]

def test_wishlist_privacy_update_invalid():
    data = {"shared_with": [123, None]}
    with pytest.raises(ValidationError):
        WishlistPrivacyUpdate(**data)
