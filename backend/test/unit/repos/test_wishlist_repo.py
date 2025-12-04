import pytest
from unittest.mock import patch, MagicMock
from backend.app.repositories.wishlist_repo import WishlistRepo

sample_wishlist = {
    "wishlist_id": 1,
    "user_id": 1,
    "items": [],
    "public": False,
    "shared_with": []
}

@patch("backend.app.repositories.wishlist_repo.WishlistRepo.load_all")
def test_get_wishlist_by_user(mock_load):
    mock_load.return_value = [sample_wishlist.copy()]
    wishlist = WishlistRepo.get_wishlist(1)
    assert wishlist["user_id"] == 1

@patch("backend.app.repositories.wishlist_repo.WishlistRepo.save_all")
def test_update_wishlist(mock_save):
    updated = sample_wishlist.copy()
    updated["public"] = True
    WishlistRepo.update_wishlist(1, updated)
    mock_save.assert_called_once()
