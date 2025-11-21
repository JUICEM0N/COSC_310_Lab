from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_view_cart_summary():
    response = client.get("/transactions/cart/1")
    assert response.status_code == 200


def test_checkout():
    response = client.post("/transactions/checkout/1")
    assert response.status_code in (200, 201)
