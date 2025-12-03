import pytest
from fastapi import HTTPException
from unittest.mock import patch
from backend.app.services.cart_service import CartService

def test_get_cart():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.CartRepo") as mock_repo:

        mock_users.user_exists.return_value = True
        mock_repo.get_cart.return_value = [{"product_id": "A"}]

        result = CartService.get_cart(1)

        assert result == [{"product_id": "A"}]
        mock_repo.get_cart.assert_called_once_with(1)

def test_add_item_success():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.ProductsRepo") as mock_prod, \
        patch("backend.app.services.cart_service.CartRepo") as mock_cart:

        mock_users.user_exists.return_value = True
        mock_prod.product_exists.return_value = True
        mock_prod.get_product.return_value = {"product_id": "P1"}

        CartService.add_item(1, "P1", 3)

        mock_cart.add_item.assert_called_once_with(1, "P1", 3)

def test_add_item_product_not_found():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.ProductsRepo") as mock_prod:

        mock_users.user_exists.return_value = True
        mock_prod.product_exists.return_value = False

        with pytest.raises(HTTPException) as exc:
            CartService.add_item(1, "BAD", 2)

        assert exc.value.status_code == 404
        assert "Product does not exist: BAD" in exc.value.detail

def test_add_item_invalid_quantity():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.ProductsRepo") as mock_prod:

        mock_users.user_exists.return_value = True
        mock_prod.product_exists.return_value = True

        with pytest.raises(HTTPException) as exc:
            CartService.add_item(1, "P1", 0)

        assert exc.value.status_code == 400
        assert exc.value.detail == "Quantity must be greater than 0"

def test_update_quantity_success():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.ProductsRepo") as mock_prod, \
        patch("backend.app.services.cart_service.CartRepo") as mock_cart:

        mock_users.user_exists.return_value = True
        mock_prod.product_exists.return_value = True
        mock_prod.get_product.return_value = {"product_id": "X"}

        CartService.update_quantity(1, "X", 5)

        mock_cart.update_quantity.assert_called_once_with(1, "X", 5)

def test_update_quantity_product_not_found():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.ProductsRepo") as mock_prod:

        mock_users.user_exists.return_value = True
        mock_prod.product_exists.return_value = False

        with pytest.raises(HTTPException) as exc:
            CartService.update_quantity(1, "XXX", 10)

        assert exc.value.status_code == 404
        assert "Product does not exist: XXX" in exc.value.detail

def test_remove_item():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.CartRepo") as mock_repo:

        mock_users.user_exists.return_value = True

        CartService.remove_item(1, "A")
        mock_repo.remove_item.assert_called_once_with(1, "A")

def test_clear_cart():
    with patch("backend.app.services.cart_service.UsersRepo") as mock_users, \
        patch("backend.app.services.cart_service.CartRepo") as mock_repo:

        mock_users.user_exists.return_value = True

        CartService.clear_cart(1)
        mock_repo.clear_cart.assert_called_once_with(1)