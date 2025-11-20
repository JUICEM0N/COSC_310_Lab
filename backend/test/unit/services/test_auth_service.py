import pytest
from unittest.mock import patch
from bcrypt import hashpw, gensalt
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate

def test_create_user_success():
    service = AuthService()

    user_data = UserCreate(
        username="newuser",
        password="password123",
        email="new@example.com",
        isAdmin=False
    )

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_email.return_value = None
        mock_repo.get_user_by_username.return_value = None
        mock_repo.get_all_users.return_value = []
        mock_repo.add_user.return_value = None

        user = service.create_user(user_data)

        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.user_id == 1
        assert user.password != "password123" 
        assert user.password.startswith("$2b$")
        mock_repo.add_user.assert_called_once()

def test_create_user_duplicate_email():
    service = AuthService()

    user_data = UserCreate(
        username="user",
        password="pass",
        email="duplicate@example.com",
        isAdmin=False
    )

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_email.return_value = {"email": "duplicate@example.com"}
        mock_repo.get_user_by_username.return_value = None

        with pytest.raises(ValueError, match="User already exists"):
            service.create_user(user_data)

def test_create_user_duplicate_username():
    service = AuthService()

    user_data = UserCreate(
        username="taken",
        password="pass",
        email="new@example.com",
        isAdmin=False
    )

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_email.return_value = None
        mock_repo.get_user_by_username.return_value = {"username": "taken"}

        with pytest.raises(ValueError, match="User already exists"):
            service.create_user(user_data)

def test_login_success():
    service = AuthService()

    hashed = hashpw("secret".encode(), gensalt()).decode()

    user_dict = {
        "user_id": 1,
        "username": "testuser",
        "password": hashed,
        "email": "test@example.com",
        "isAdmin": False,
        "createdAt": "2025-01-01T12:00:00"
    }

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_email.return_value = user_dict

        user = service.login("test@example.com", "secret")

        assert user is not None
        assert user.user_id == 1
        assert user.username == "testuser"

def test_login_wrong_password():
    service = AuthService()

    hashed = hashpw("correct".encode(), gensalt()).decode()

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_email.return_value = {
            "user_id": 1,
            "username": "user",
            "password": hashed,
            "email": "test@example.com",
            "isAdmin": False,
            "createdAt": "2025-01-01T12:00:00"
        }

        user = service.login("test@example.com", "wrongpass")
        assert user is None

def test_login_no_user():
    service = AuthService()

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_email.return_value = None

        user = service.login("none@example.com", "pass")
        assert user is None

def test_change_password_success():
    service = AuthService()

    old_hash = hashpw("oldpass".encode(), gensalt()).decode()

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_id.return_value = {
            "user_id": 1,
            "password": old_hash
        }

        mock_repo.update_user.return_value = None

        service.change_password(1, "oldpass", "newpass")

        mock_repo.update_user.assert_called_once()
        args = mock_repo.update_user.call_args[0]
        assert args[0] == 1
        assert "password" in args[1]
        assert args[1]["password"].startswith("$2b$")

def test_change_password_user_not_found():
    service = AuthService()

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_id.return_value = None

        with pytest.raises(ValueError, match="User not found"):
            service.change_password(99, "oldpass", "newpass")

def test_change_password_wrong_old_password():
    service = AuthService()

    correct_hash = hashpw("realpass".encode(), gensalt()).decode()

    with patch("backend.app.services.auth_service.UsersRepo") as mock_repo:
        mock_repo.get_user_by_id.return_value = {
            "user_id": 1,
            "password": correct_hash
        }

        with pytest.raises(ValueError, match="Incorrect password"):
            service.change_password(1, "wrongpass", "newpass")