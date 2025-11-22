from backend.app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

def test_get_cart():
    response = client.get("/cart/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)

def test_add_to_cart():
    with patch("backend.app.routers.cart.CartService") as mock_service:
        mock_service.add_item.return_value = None
        response = client.post("/cart/1/add", params={"product_id": "TEST123", "quantity": 1})
        assert response.status_code == 200
        mock_service.add_item.assert_called_once_with(1, "TEST123", 1)

def test_update_quantity():
    with patch("backend.app.routers.cart.CartService") as mock_service:
        mock_service.update_quantity.return_value = None
        response = client.patch("/cart/1/update", params={"product_id": "TEST123", "quantity": 2})
        assert response.status_code == 200
        mock_service.update_quantity.assert_called_once_with(1, "TEST123", 2)

def test_remove_item():
    with patch("backend.app.routers.cart.CartService") as mock_service:
        mock_service.remove_item.return_value = None
        response = client.delete("/cart/1/remove", params={"product_id": "TEST123"})
        assert response.status_code == 200
        mock_service.remove_item.assert_called_once_with(1, "TEST123")

def test_get_cart():
    with patch("backend.app.routers.cart.CartService") as mock_service:
        mock_service.get_cart.return_value = []
        response = client.get("/cart/1")
        assert response.status_code == 200
        assert response.json() == []
        mock_service.get_cart.assert_called_once_with(1)

def test_clear_cart():
    response = client.delete("/cart/1/clear")
    assert response.status_code == 200