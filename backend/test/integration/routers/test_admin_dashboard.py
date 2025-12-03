import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app
from backend.app.routers.admin_dashboard import UsersRepo, TransactionsRepo, PenaltiesRepo, ProductsRepo, require_admin

client = TestClient(app)

def mock_admin_user():
    return {"user_id": 1, "name": "Admin", "isAdmin": True}

app.dependency_overrides[require_admin] = mock_admin_user

def test_get_all_users():
    with patch.object(UsersRepo, "load_users", return_value=[
        {"user_id": 1, "name": "Alice"},
        {"user_id": 2, "name": "Bob"}
    ]):
        response = client.get("/admin_dashboard/users")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "All users retrieved successfully"
        assert data["users"] == [
            {"user_id": 1, "name": "Alice"},
            {"user_id": 2, "name": "Bob"}
        ]

def test_get_user_details():
    with patch.object(UsersRepo, "load_users", return_value=[{"user_id": 10, "name": "Charlie"}]), \
         patch.object(TransactionsRepo, "get_transactions_by_user", return_value=[{"id": 1, "amount": 20}]), \
         patch.object(PenaltiesRepo, "get_penalties_by_user", return_value=[{"id": 1, "reason": "Late return"}]):

        response = client.get("/admin_dashboard/user/10")
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_id"] == 10
        assert len(data["transactions"]) == 1
        assert len(data["penalties"]) == 1

def test_get_user_details_not_found():
    with patch.object(UsersRepo, "load_users", return_value=[]):
        response = client.get("/admin_dashboard/user/99")
        assert response.status_code == 404

def test_admin_summary():
    with patch.object(UsersRepo, "load_users", return_value=[{"user_id": 1}, {"user_id": 2}]), \
         patch.object(TransactionsRepo, "get_transactions_by_user", side_effect=[
             [{"id": 1, "date": "2024-10-01"}],
             [{"id": 2, "date": "2024-10-02"}]
         ]), \
         patch.object(PenaltiesRepo, "get_penalties_by_user", side_effect=[
             [{"id": 1, "date_issued": "2024-10-05"}],
             [{"id": 2, "date_issued": "2024-10-06"}]
         ]):

        response = client.get("/admin_dashboard/summary")
        assert response.status_code == 200
        summary = response.json()
        totals = summary["totals"]
        assert totals["total_users"] == 2
        assert totals["total_transactions"] == 2
        assert totals["total_penalties"] == 2
        latest = summary["latest"]
        assert len(latest["recent_transactions"]) == 2
        assert len(latest["recent_penalties"]) == 2

def test_get_inventory_updates():
    with patch.object(ProductsRepo, "load_products", return_value=[
        {"product_id": "P1", "quantity": 10},
        {"product_id": "P2", "quantity": 2},
        {"product_id": "P3", "quantity": 0}
    ]):
        response = client.get("/admin_dashboard/inventory")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

def test_download_transactions(tmp_path):
    fake_file = tmp_path / "transactions.json"
    fake_file.write_text('[{"id": 1}]')

    with patch("backend.app.routers.admin_dashboard.os.path.exists", return_value=True), \
         patch("backend.app.routers.admin_dashboard.FileResponse") as mock_file:

        client.get("/admin_dashboard/download/transactions")
        mock_file.assert_called_once()
