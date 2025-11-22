from fastapi.testclient import TestClient
from backend.app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    with patch("backend.app.routers.items.ItemsService") as mock_service:
        mock_service.create_item.return_value = {
            "product_id": "TEST123",
            "product_name": "Test Product",
            "category": "Electronics",
            "discounted_price": "9.99",
            "actual_price": "19.99",
            "discount_percentage": "50%",
            "rating": "4.5",
            "rating_count": "100",
            "about_product": "A test product",
            "user_id": "1",
            "user_name": "tester",
            "review_id": "r123",
            "review_title": "Nice",
            "review_content": "This item is good",
            "img_link": "http://example.com/img.png",
            "product_link": "http://example.com/product"
        }

        response = client.post(
            "/items",
            json={
                "product_id": "TEST123",
                "product_name": "Test Product",
                "category": "Electronics",
                "discounted_price": "9.99",
                "actual_price": "19.99",
                "discount_percentage": "50%",
                "rating": "4.5",
                "rating_count": "100",
                "about_product": "A test product",
                "user_id": "1",
                "user_name": "tester",
                "review_id": "r123",
                "review_title": "Nice",
                "review_content": "This item is good",
                "img_link": "http://example.com/img.png",
                "product_link": "http://example.com/product"
            }
        )

        assert response.status_code in (200, 201)