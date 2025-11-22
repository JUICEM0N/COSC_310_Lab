import json
import pytest
from pathlib import Path
from fastapi import HTTPException
from backend.app.repositories.cart_repo import CartRepo


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
    cart = CartRepo.get_cart(1)
    assert cart is None



def test_add_item_raises_if_cart_missing(temp_cart_file):
    with pytest.raises(HTTPException) as exc:
        CartRepo.add_item(1, "A", 2)
    assert exc.value.status_code == 404
    assert "Cart not found" in exc.value.detail


def test_remove_item_raises_if_cart_missing(temp_cart_file):
    with pytest.raises(HTTPException):
        CartRepo.remove_item(1, "A")


def test_clear_cart_raises_if_missing(temp_cart_file):
    with pytest.raises(HTTPException):
        CartRepo.clear_cart(1)


def test_update_quantity_raises_if_missing(temp_cart_file):
    with pytest.raises(TypeError):
        CartRepo.update_quantity(1, "A", 5)


def test_update_cart_raises_if_missing(temp_cart_file):
    with pytest.raises(HTTPException):
        CartRepo.update_cart(99, [{"product_id": "X", "quantity": 3}])
