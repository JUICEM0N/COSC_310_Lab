import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.admin_service import AdminService


def test_promote_user_success():
    users = [
        {"id": 1, "isAdmin": False},
        {"id": 2, "isAdmin": False},
    ]

    with patch("backend.app.services.admin_service.repo") as mock_repo:
        mock_repo.load_users.return_value = users
        mock_repo.save_users.return_value = None

        service = AdminService()
        result = service.promote_user(1)

        assert result is True
        assert users[0]["isAdmin"] is True
        mock_repo.save_users.assert_called_once_with(users)


def test_promote_user_not_found():
    users = [{"id": 2, "isAdmin": False}]

    with patch("backend.app.services.admin_service.repo") as mock_repo:
        mock_repo.load_users.return_value = users
        mock_repo.save_users.return_value = None

        service = AdminService()
        result = service.promote_user(1)

        assert result is False
        mock_repo.save_users.assert_not_called()


def test_promote_user_already_admin():
    users = [{"id": 1, "isAdmin": True}]

    with patch("backend.app.services.admin_service.repo") as mock_repo:
        mock_repo.load_users.return_value = users
        mock_repo.save_users.return_value = None

        service = AdminService()
        result = service.promote_user(1)

        assert result is True
        assert users[0]["isAdmin"] is True
        mock_repo.save_users.assert_called_once_with(users)


def test_apply_penalty_success():
    penalties = []

    with patch("backend.app.services.admin_service.repo") as mock_repo, \
         patch("backend.app.services.admin_service.uuid.uuid4", return_value="test-uuid"), \
         patch("backend.app.services.admin_service.datetime") as mock_datetime:

        mock_datetime.utcnow.return_value.isoformat.return_value = "2025-11-21T00:00:00"
        mock_repo.load_penalties.return_value = penalties
        mock_repo.save_penalties.return_value = None

        service = AdminService()
        penalty_id = service.apply_penalty(1, "Late payment", 50.0, "pending")

        assert penalty_id == "test-uuid"
        assert len(penalties) == 1
        assert penalties[0]["id"] == "test-uuid"
        assert penalties[0]["user_id"] == 1
        assert penalties[0]["reason"] == "Late payment"
        assert penalties[0]["amount"] == 50.0
        assert penalties[0]["status"] == "pending"
        assert penalties[0]["date_issued"] == "2025-11-21T00:00:00"

        mock_repo.save_penalties.assert_called_once_with(penalties)


def test_apply_penalty_zero_amount():
    penalties = []

    with patch("backend.app.services.admin_service.repo") as mock_repo, \
         patch("backend.app.services.admin_service.uuid.uuid4", return_value="zero-uuid"), \
         patch("backend.app.services.admin_service.datetime") as mock_datetime:

        mock_datetime.utcnow.return_value.isoformat.return_value = "2025-11-21T00:00:00"
        mock_repo.load_penalties.return_value = penalties

        service = AdminService()
        penalty_id = service.apply_penalty(1, "No fee", 0.0, "pending")

        assert penalty_id == "zero-uuid"
        assert len(penalties) == 1
        assert penalties[0]["amount"] == 0.0

        mock_repo.save_penalties.assert_called_once_with(penalties)


def test_get_user_penalties_filters_correctly():
    penalties = [
        {"id": "p1", "user_id": 1},
        {"id": "p2", "user_id": 2},
        {"id": "p3", "user_id": 1},
    ]

    with patch("backend.app.services.admin_service.repo") as mock_repo:
        mock_repo.load_penalties.return_value = penalties

        service = AdminService()
        result = service.get_user_penalties(1)

        assert len(result) == 2
        assert all(p["user_id"] == 1 for p in result)
