# backend/test/integration/routers/test_wishlist.py
from fastapi.testclient import TestClient
from backend.app.main import app  # make sure this is your FastAPI app
from backend.app.services.wishlist_service import WishlistService
from unittest.mock import patch

client = TestClient(app)

sample_wishlist = {"user_id": 1, "items": [{"product_id": "123", "quantity": 2}]}
@patch("backend.app.services.wishlist_service.WishlistService.get_wishlist")
def test_get_wishlist(mock_get):
    mock_get.return_value = sample_wishlist.copy()
    response = client.get("/wishlist/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["items"][0]["product_id"] == "123"

