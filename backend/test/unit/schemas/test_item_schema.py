import pytest
from pydantic import ValidationError
from backend.app.schemas.item import Item, ItemCreate, ItemUpdate

def valid_item_data():
    return {
        "product_id": "123",
        "product_name": "Laptop",
        "category": "Electronics",
        "discounted_price": "900",
        "actual_price": "1000",
        "discount_percentage": "10%",
        "rating": "4.5",
        "rating_count": "200",
        "about_product": "A good laptop.",
        "user_id": "u1",
        "user_name": "John",
        "review_id": "r1",
        "review_title": "Nice!",
        "review_content": "Very good!",
        "img_link": "http://example.com/img.jpg",
        "product_link": "http://example.com/product",
        "quantity": 6
    }

def valid_create_update_data():
    return valid_item_data().copy()

def test_item_valid():
    data = valid_item_data()
    item = Item(**data)
    assert item.product_name == "Laptop"
    assert item.product_id == "123"

def test_item_missing_id():
    data = valid_item_data()
    data.pop("product_id")
    with pytest.raises(ValidationError):
        Item(**data)

def test_item_invalid_type():
    data = valid_item_data()
    data["rating"] = 4.5
    with pytest.raises(ValidationError):
        Item(**data)

def test_item_create_valid():
    data = valid_create_update_data()
    item = ItemCreate(**data)

    assert item.product_name == "Laptop"
    assert item.product_id == "123"

def test_item_create_missing_field():
    data = valid_create_update_data()
    data.pop("product_name")
    with pytest.raises(ValidationError):
        ItemCreate(**data)

def test_item_create_invalid_type():
    data = valid_create_update_data()
    data["rating_count"] = 500
    with pytest.raises(ValidationError):
        ItemCreate(**data)

def test_item_update_valid():
    data = valid_create_update_data()
    item = ItemUpdate(**data)
    assert item.review_title == "Nice!"

# def test_item_update_missing_required_field():
#     data = valid_create_update_data()
#     data.pop("not_exists") 
#     item = ItemUpdate(**data)

#     assert not hasattr(item, "not_exists")

def test_item_update_invalid_type():
    data = valid_create_update_data()
    data["actual_price"] = 1000 
    with pytest.raises(ValidationError):
        ItemUpdate(**data)