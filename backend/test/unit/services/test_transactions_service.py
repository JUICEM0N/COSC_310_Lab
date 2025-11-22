import pytest
from unittest.mock import patch
from backend.app.services.transactions_service import (
    TransactionsService,
    parse_price,
    TAX_RATE
)

def test_parse_price_valid():
    assert parse_price("$10") == 10.0
    assert parse_price("20.50") == 20.50
    assert parse_price("  $5.75  ") == 5.75

def test_parse_price_empty():
    assert parse_price("") == 0.0
    assert parse_price(None) == 0.0

def test_get_cart_summary_basic():
    cart = {
        "items": [
            {"product_id": "p1", "quantity": 2},
            {"product_id": "p2", "quantity": 1},
        ]
    }

    product_p1 = {
        "product_id": "p1",
        "product_name": "Mouse",
        "discounted_price": "10",
        "actual_price": "20",
        "discount_percentage": "50%",
        "category": "Electronics",
        "rating": "4.2",
        "rating_count": "120",
        "img_link": "img1.jpg"
    }

    product_p2 = {
        "product_id": "p2",
        "product_name": "Keyboard",
        "discounted_price": "30",
        "actual_price": "50",
        "discount_percentage": "40%",
        "category": "Electronics",
        "rating": "4.8",
        "rating_count": "90",
        "img_link": "img2.jpg"
    }

    with patch("backend.app.services.transactions_service.CartRepo") as mock_cart, \
        patch("backend.app.services.transactions_service.ProductsRepo") as mock_prod:

        mock_cart.get_cart.return_value = cart
        mock_cart.cart_exists.return_value = True
        mock_prod.get_products.side_effect = lambda pid: product_p1 if pid == "p1" else product_p2

        summary = TransactionsService.get_cart_summary(1)

        assert summary["subtotal"] == 50.0
        assert summary["tax"] == round(50.0 * TAX_RATE, 2)
        assert summary["total"] == round(50.0 * (1 + TAX_RATE), 2)
        assert len(summary["items"]) == 2

        p1_summary = summary["items"][0]
        assert p1_summary["product_id"] == "p1"
        assert p1_summary["quantity"] == 2
        assert p1_summary["price_per_unit"] == 10.0
        assert p1_summary["subtotal"] == 20.0

def test_get_cart_summary_skips_missing_products():
    cart = {
        "items": [
            {"product_id": "p1", "quantity": 2},
            {"product_id": "missing", "quantity": 3},
        ]
    }

    product_p1 = {
        "product_id": "p1",
        "product_name": "Mouse",
        "discounted_price": "10",
        "actual_price": "20",
        "discount_percentage": "50%",
        "category": "Electronics",
        "rating": "4.2",
        "rating_count": "120",
        "img_link": "img1.jpg"
    }

    with patch("backend.app.services.transactions_service.CartRepo") as mock_cart, \
        patch("backend.app.services.transactions_service.ProductsRepo") as mock_prod:

        mock_cart.get_cart.return_value = cart
        mock_cart.cart_exists.return_value = True
        mock_prod.get_products.side_effect = lambda pid: product_p1 if pid == "p1" else None

        summary = TransactionsService.get_cart_summary(42)

        assert len(summary["items"]) == 1
        assert summary["subtotal"] == 20.0

def test_get_cart_summary_empty_cart():
    with patch("backend.app.services.transactions_service.CartRepo") as mock_cart, \
        patch("backend.app.services.transactions_service.ProductsRepo") as mock_prod:

        mock_cart.get_cart.return_value = {"items": []}
        mock_cart.cart_exists.return_value = True
        mock_prod.get_products.return_value = None

        summary = TransactionsService.get_cart_summary(7)

        assert summary["items"] == []
        assert summary["subtotal"] == 0.0
        assert summary["tax"] == 0.0
        assert summary["total"] == 0.0

def test_checkout_success():
    mock_summary = {
        "items": [{"product_id": "p1", "subtotal": 10}],
        "total": 11.2,
    }

    with patch("backend.app.services.transactions_service.TransactionsService.get_cart_summary") as mock_summary_fn, \
        patch("backend.app.services.transactions_service.TransactionsRepo") as mock_trans, \
        patch("backend.app.services.transactions_service.CartRepo") as mock_cart:

        mock_summary_fn.return_value = mock_summary
        mock_cart.cart_exists.return_value = True
        mock_cart.get_cart.return_value = {"items": mock_summary["items"]}

        receipt = TransactionsService.checkout(5)

        mock_trans.add_transaction.assert_called_once()
        mock_cart.clear_cart.assert_called_once_with(5)

        assert receipt["user_id"] == 5
        assert receipt["total_amount"] == mock_summary["total"]
        assert receipt["products"] == mock_summary["items"]
        assert receipt["status"] == "completed"
        assert "date" in receipt
