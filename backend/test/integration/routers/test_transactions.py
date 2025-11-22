from backend.app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

def test_view_cart_summary():
    response = client.get("/transactions/cart/1")
    assert response.status_code == 200

def test_checkout():
    with patch("backend.app.routers.transactions.TransactionsService") as mock_service:
        mock_service.checkout.return_value = {
            "user_id": 1,
            "total_amount": 20.0,
            "products": [{"product_id": "p1", "subtotal": 10}],
            "status": "completed",
            "date": "2024-01-01"
        }

        response = client.post("/transactions/checkout/1")

        assert response.status_code in (200, 201)
        mock_service.checkout.assert_called_once_with(1)
