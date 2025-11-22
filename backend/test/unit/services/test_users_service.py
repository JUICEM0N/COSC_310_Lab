import pytest
from backend.app.services.users_service import UsersService
from backend.app.repositories.users_repo import UsersRepo
from bcrypt import checkpw, hashpw, gensalt

@pytest.fixture(autouse=True)
def clean():
    UsersRepo.save_users([])

def test_get_user_info():
    UsersRepo.add_user({
        "user_id": 1,
        "username": "testuser",
        "password": hashpw("pass123".encode(), gensalt()).decode(),
        "email": "test@test.com",
        "isAdmin": False,
        "createdAt": "2025-01-01"
    })
    user = UsersService.get_user_info(1)
    assert user["username"] == "testuser"
    assert UsersService.get_user_info(999) is None

def test_update_user():
    UsersRepo.add_user({
        "user_id": 2,
        "username": "old",
        "email": "old@test.com",
        "password": "xxx",
        "isAdmin": False,
        "createdAt": "2025-01-01"
    })
    updated = UsersService.update_user(2, {"username": "newname", "isAdmin": True})
    assert updated["username"] == "newname"
    assert updated["isAdmin"] is True

def test_change_user_password_success():
    hashed = hashpw("oldpass".encode(), gensalt()).decode()
    UsersRepo.add_user({
        "user_id": 3,
        "username": "changepass",
        "password": hashed,
        "email": "cp@test.com",
        "isAdmin": False,
        "createdAt": "2025-01-01"
    })

    result = UsersService.change_user_password(3, "oldpass", "newpass456")
    assert result is True

    user = UsersRepo.get_user_by_id(3)
    assert checkpw("newpass456".encode(), user["password"].encode())

def test_change_user_password_wrong_old():
    hashed = hashpw("correct".encode(), gensalt()).decode()
    UsersRepo.add_user({
        "user_id": 4,
        "username": "wrongpass",
        "password": hashed,
        "email": "wrong@test.com",
        "isAdmin": False,
        "createdAt": "2025-01-01"
    })

    result = UsersService.change_user_password(4, "wrong", "new")
    assert result is False