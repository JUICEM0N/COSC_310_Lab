import pytest
from pydantic import ValidationError
from backend.app.schemas.cart import CartItem, Cart, CartCreate, CartUpdate


def test_cart_item_valid():
    item = CartItem(
        product_id="A1",
        namme="Laptop",
        quantity=2,
        price_per_unit=999.99,
        total_price=1999.98
    )
    assert item.product_id == "A1"
    assert item.namme == "Laptop"
    assert item.quantity == 2


def test_cart_item_invalid_missing_field():
    with pytest.raises(ValidationError):
        CartItem(
            product_id="A1",
            quantity=2,
            price_per_unit=10.0,
            total_price=20.0
        )


def test_cart_item_invalid_type():
    with pytest.raises(ValidationError):
        CartItem(
            product_id="A1",
            namme="Item",
            quantity="five",
            price_per_unit=10.0,
            total_price=20.0
        )


def test_cart_valid():
    cart = Cart(
        cart_id=10,
        items=[
            CartItem(
                product_id="A1",
                namme="Laptop",
                quantity=1,
                price_per_unit=1000.0,
                total_price=1000.0
            )
        ],
        total_price=1000.0
    )
    assert cart.cart_id == 10
    assert len(cart.items) == 1


def test_cart_invalid_nested_item_type():
    with pytest.raises(ValidationError):
        Cart(
            cart_id=3,
            items=[{"product_id": "x"}],
            total_price=0.0
        )


def test_cart_create_valid():
    data = CartCreate(
        items=[
            CartItem(
                product_id="B1",
                namme="Keyboard",
                quantity=3,
                price_per_unit=30.0,
                total_price=90.0
            )
        ],
        total_price=90.0
    )
    assert data.total_price == 90.0
    assert len(data.items) == 1


def test_cart_create_invalid_missing_items():
    with pytest.raises(ValidationError):
        CartCreate(total_price=100.0)


def test_cart_update_valid():
    data = CartUpdate(
        items=[
            CartItem(
                product_id="C1",
                namme="Mouse",
                quantity=2,
                price_per_unit=15.0,
                total_price=30.0
            )
        ],
        total_price=30.0
    )
    assert data.items[0].product_id == "C1"


def test_cart_update_invalid_total_price_type():
    with pytest.raises(ValidationError):
        CartUpdate(
            items=[],
            total_price="not a number"
        )
