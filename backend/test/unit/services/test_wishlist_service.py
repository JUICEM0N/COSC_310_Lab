from backend.app.services.wishlist_service import WishlistService
from unittest.mock import patch
import pytest

sample_wishlist = {"user_id": 1, "items": [{"product_id": "123", "quantity": 2}]}

@patch("backend.app.repositories.wishlist_repo.WishlistRepo.get_wishlist")
def test_get_wishlist(mock_get):
    mock_get.return_value = sample_wishlist.copy()
    wishlist = WishlistService.get_wishlist(1)
    assert wishlist["user_id"] == 1
    assert wishlist["items"][0]["product_id"] == "123"

