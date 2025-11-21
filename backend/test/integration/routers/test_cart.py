from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_cart():
    response = client.get("/cart/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_to_cart():
    response = client.post("/cart/1/add", params={
        "product_id": "TEST123",
        "quantity": 1
    })
    assert response.status_code in (200, 201)

def test_update_quantity():
    response = client.patch("/cart/1/update", params={
        "product_id": "TEST123",
        "quantity": 2
    })
    assert response.status_code == 200

def test_remove_item():
    response = client.delete("/cart/1/remove", params={
        "product_id": "TEST123"
    })
    assert response.status_code == 200

def test_clear_cart():
    response = client.delete("/cart/1/clear")
    assert response.status_code == 200
