import json
import pytest
from pathlib import Path
from backend.app.repositories.cart_repo import CartRepo, DATA_PATH


@pytest.fixture
def temp_cart_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "cart.json"
    monkeypatch.setattr("backend.app.repositories.cart_repo.DATA_PATH", temp_file)
    return temp_file


def read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def test_load_carts_creates_file_if_missing(temp_cart_file):
    carts = CartRepo.load_carts()
    assert carts == []
    assert temp_cart_file.exists()
    assert read_json(temp_cart_file) == []


def test_get_cart_creates_new_cart_when_missing(temp_cart_file):
    items = CartRepo.get_cart(1)
    assert items == []
    data = read_json(temp_cart_file)
    assert data == [{"user_id": 1, "items": []}]


def test_add_item_creates_new_item(temp_cart_file):
    CartRepo.add_item(1, "A", 2)
    data = read_json(temp_cart_file)
    assert data[0]["items"] == [{"product_id": "A", "quantity": 2}]


def test_add_item_increases_existing_quantity(temp_cart_file):
    CartRepo.add_item(1, "A", 2)
    CartRepo.add_item(1, "A", 3)
    data = read_json(temp_cart_file)
    assert data[0]["items"] == [{"product_id": "A", "quantity": 5}]


def test_remove_item(temp_cart_file):
    CartRepo.add_item(1, "A", 1)
    CartRepo.add_item(1, "B", 1)

    CartRepo.remove_item(1, "A")

    data = read_json(temp_cart_file)
    assert data[0]["items"] == [{"product_id": "B", "quantity": 1}]


def test_clear_cart(temp_cart_file):
    CartRepo.add_item(1, "A", 2)
    CartRepo.clear_cart(1)

    data = read_json(temp_cart_file)
    assert data[0]["items"] == []


def test_update_quantity_changes_value(temp_cart_file):
    CartRepo.add_item(1, "A", 2)
    CartRepo.update_quantity(1, "A", 10)

    data = read_json(temp_cart_file)
    assert data[0]["items"] == [{"product_id": "A", "quantity": 10}]


def test_update_quantity_removes_when_zero(temp_cart_file):
    CartRepo.add_item(1, "A", 2)
    CartRepo.update_quantity(1, "A", 0)

    data = read_json(temp_cart_file)
    assert data[0]["items"] == []


def test_update_cart_adds_new_user_cart(temp_cart_file):
    CartRepo.update_cart(99, [{"product_id": "X", "quantity": 3}])
    data = read_json(temp_cart_file)
    assert data == [{"user_id": 99, "items": [{"product_id": "X", "quantity": 3}]}]
