import pytest
from pydantic import ValidationError
from datetime import datetime
from backend.app.schemas.user import (
    User, UserCreate, UserOut, UserUpdate, ChangePassword
)

def valid_user_data():
    return {
        "user_id": 1,
        "username": "testuser",
        "password": "hashedpassword",
        "email": "test@example.com",
        "isAdmin": True,
        "createdAt": "2025-01-01T12:00:00"
    }

def valid_create_data():
    return {
        "username": "newuser",
        "password": "mypassword",
        "email": "new@example.com",
        "isAdmin": False,
    }

def test_user_valid():
    u = User(**valid_user_data())
    assert u.user_id == 1
    assert u.username == "testuser"
    assert u.isAdmin is True
    assert isinstance(u.createdAt, str)

def test_user_missing_required_field():
    data = valid_user_data()
    data.pop("email")
    with pytest.raises(ValidationError):
        User(**data)

def test_user_invalid_type():
    data = valid_user_data()
    data["user_id"] = "not-an-int"
    with pytest.raises(ValidationError):
        User(**data)

def test_user_create_valid():
    u = UserCreate(**valid_create_data())
    assert u.username == "newuser"
    assert u.isAdmin is False

def test_user_create_missing_password():
    data = valid_create_data()
    data.pop("password")
    with pytest.raises(ValidationError):
        UserCreate(**data)

def test_user_create_invalid_type():
    data = valid_create_data()
    data["isAdmin"] = "yes"
    with pytest.raises(ValidationError):
        UserCreate(**data)

def test_user_out_valid():
    u = UserOut(
        user_id=1,
        username="testuser",
        email="t@example.com",
        isAdmin=True,
        createdAt="2025-01-01T12:00:00"
    )
    assert isinstance(u.createdAt, str)
    assert "2025-01-01" in u.createdAt

def test_user_out_missing_field():
    with pytest.raises(ValidationError):
        UserOut(
            user_id=1,
            username="testuser",
            isAdmin=False,
            createdAt="2025-01-01T12:00:00"
        )

def test_user_out_any_string_accepted():
    u = UserOut(
        user_id=1,
        username="testuser",
        email="t@example.com",
        isAdmin=False,
        createdAt="not-a-datetime"
    )
    assert u.createdAt == "not-a-datetime"

def test_user_update_valid():
    u = UserUpdate(
        username="updateduser",
        email="updated@example.com",
        isAdmin=True
    )
    assert u.username == "updateduser"
    assert u.isAdmin is True

def test_user_update_missing_email():
    with pytest.raises(ValidationError):
        UserUpdate(
            username="user",
            isAdmin=False
        )

def test_user_update_invalid_type():
    with pytest.raises(ValidationError):
        UserUpdate(
            username="user",
            email="user@example.com",
            isAdmin="not-bool"
        )

def test_change_password_valid():
    c = ChangePassword(old_password="old123", new_password="new123")
    assert c.old_password == "old123"
    assert c.new_password == "new123"

def test_change_password_missing_field():
    with pytest.raises(ValidationError):
        ChangePassword(new_password="abc123")

def test_change_password_invalid_type():
    with pytest.raises(ValidationError):
        ChangePassword(old_password=123, new_password="abc123")