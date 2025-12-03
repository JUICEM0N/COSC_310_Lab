import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.routers import admin
from backend.app.main import app

def mock_admin_user():
    return {"user_id": 1, "isAdmin": True}
app.dependency_overrides[admin.require_admin] = mock_admin_user

client = TestClient(app)

def mock_admin_user():
    return {"user_id": 1, "isAdmin": True}

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.AdminService.promote_user", return_value=True)
def test_promote_user(mock_promote, mock_user):
    response = client.post("/admin/promote", json={"user_id": 10})
    assert response.status_code == 200
    assert response.json() == {"msg": "User 10 promoted to admin"}
    mock_promote.assert_called_once_with(10)

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.AdminService.apply_penalty", return_value=55)
def test_apply_penalty(mock_apply, mock_user):
    data = {
        "user_id": 12,
        "reason": "Late return",
        "amount": 25.0,
        "status": "pending"
    }

    response = client.post("/admin/penalty", json=data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Penalty applied", "penalty_id": 55}
    mock_apply.assert_called_once()

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.AdminService.get_user_penalties", return_value=[{"id": 1, "amount": 10}])
def test_get_penalties(mock_get, mock_user):
    response = client.get("/admin/penalties/5")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "amount": 10}]
    mock_get.assert_called_once_with(5)

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.ProductsRepo.apply_discount", return_value=True)
def test_apply_discount(mock_apply, mock_user):
    response = client.post("/admin/discount/P123?percent=15")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Discount applied to P123",
        "discount_percent": 15.0
    }
    mock_apply.assert_called_once_with("P123", 15.0)

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.ProductsRepo.remove_discount", return_value=True)
def test_remove_discount(mock_remove, mock_user):
    response = client.delete("/admin/discount/P456")
    assert response.status_code == 200
    assert response.json() == {"msg": "Discount removed from P456"}
    mock_remove.assert_called_once_with("P456")

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.ProductsRepo.set_products_of_the_week")
def test_set_products_of_week(mock_set, mock_user):
    response = client.post("/admin/products-of-week", json={"product_ids": ["P1", "P2"]})
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Products of the week updated",
        "products": ["P1", "P2"]
    }
    mock_set.assert_called_once_with(["P1", "P2"])

@patch("backend.app.routers.admin.require_admin", side_effect=mock_admin_user)
@patch("backend.app.routers.admin.ProductsRepo.get_products_of_the_week", return_value=["A1", "B2"])
def test_get_products_of_week(mock_get, mock_user):
    response = client.get("/admin/products-of-week")
    assert response.status_code == 200
    assert response.json() == {"products_of_week": ["A1", "B2"]}
    mock_get.assert_called_once()
