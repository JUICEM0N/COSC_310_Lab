import pytest
from unittest.mock import patch
from backend.app.services.users_service import UsersService

def test_get_user_info_found():
    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_id.return_value = {"id": 1, "username": "Alice"}

        user = UsersService.get_user_info(1)

        assert user == {"id": 1, "username": "Alice"}
        mock_repo.get_user_by_id.assert_called_once_with(1)


def test_get_user_info_not_found():
    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_id.return_value = None

        user = UsersService.get_user_info(99)

        assert user is None
        mock_repo.get_user_by_id.assert_called_once_with(99)

def test_update_user_success():
    initial_users = [
        {"id": 1, "username": "Alice", "email": "a@a.com"},
        {"id": 2, "username": "Bob", "email": "b@b.com"},
    ]

    updated_data = {"username": "Alicia"}

    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.load_users.return_value = initial_users
        mock_repo.save_users.return_value = None

        updated_user = UsersService.update_user(1, updated_data)

        assert updated_user["username"] == "Alicia"
        assert updated_user["email"] == "a@a.com"
        mock_repo.save_users.assert_called_once()

def test_update_user_not_found():
    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.load_users.return_value = [
            {"id": 1, "username": "Alice"}
        ]
        mock_repo.save_users.return_value = None

        result = UsersService.update_user(99, {"username": "New"})

        assert result is None
        mock_repo.save_users.assert_not_called()

def test_update_user_ignores_unknown_fields():
    initial_users = [{"id": 1, "username": "Alice"}]

    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.load_users.return_value = initial_users
        mock_repo.save_users.return_value = None

        updated_user = UsersService.update_user(1, {"unknown": "BAD", "username": "Zed"})

        assert updated_user["username"] == "Zed"
        assert "unknown" not in updated_user
        mock_repo.save_users.assert_called_once()

def test_change_password_success():
    initial_users = [{"id": 1, "password": "old123"}]

    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.load_users.return_value = initial_users
        mock_repo.save_users.return_value = None

        result = UsersService.change_user_password(1, "old123", "new123")

        assert result is True
        assert initial_users[0]["password"] == "new123"
        mock_repo.save_users.assert_called_once()

def test_change_password_wrong_old_password():
    initial_users = [{"id": 1, "password": "old123"}]

    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.load_users.return_value = initial_users

        result = UsersService.change_user_password(1, "WRONG", "new123")

        assert result is False
        mock_repo.save_users.assert_not_called()

def test_change_password_user_not_found():
    with patch("backend.app.services.users_service.UsersRepo") as mock_repo:
        mock_repo.load_users.return_value = []

        result = UsersService.change_user_password(99, "pass", "newpass")

        assert result is False
        mock_repo.save_users.assert_not_called()