import pytest
from backend.app.repositories.users_repo import UsersRepo
import json
from pathlib import Path

@pytest.fixture
def temp_users_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "users.json"
    temp_file.write_text("[]")

    monkeypatch.setattr(
        "backend.app.repositories.users_repo.DATA_PATH",
        temp_file
    )
    return temp_file

def read_json(path: Path):
    return json.loads(path.read_text())

def test_load_users_returns_empty_if_missing(tmp_path, monkeypatch):
    fake_json = tmp_path / "users.json"
    monkeypatch.setattr(
        "backend.app.repositories.users_repo.DATA_PATH",
        fake_json
    )
    assert UsersRepo.load_users() == []

def test_load_users_reads_file(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 1, "email": "a@test.com", "username": "alpha"}
    ]))

    users = UsersRepo.load_users()
    assert len(users) == 1
    assert users[0]["user_id"] == 1

def test_save_users_overwrites_file(temp_users_file):
    UsersRepo.save_users([
        {"user_id": 2, "email": "b@test.com", "username": "beta"}
    ])

    data = read_json(temp_users_file)
    assert data == [{"user_id": 2, "email": "b@test.com", "username": "beta"}]

def test_get_all_users(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 1, "email": "a@test.com", "username": "alpha"}
    ]))
    users = UsersRepo.get_all_users()
    assert len(users) == 1

def test_get_user_by_id_found(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 5, "email": "x@test.com", "username": "xman"}
    ]))

    user = UsersRepo.get_user_by_id(5)
    assert user["username"] == "xman"

def test_get_user_by_id_not_found(temp_users_file):
    temp_users_file.write_text(json.dumps([]))
    assert UsersRepo.get_user_by_id(123) is None

def test_get_user_by_email(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 1, "email": "user@domain.com", "username": "u1"}
    ]))

    user = UsersRepo.get_user_by_email("user@domain.com")
    assert user["user_id"] == 1

def test_get_user_by_username(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 1, "email": "x@x.com", "username": "tester"}
    ]))

    user = UsersRepo.get_user_by_username("tester")
    assert user["email"] == "x@x.com"

def test_add_user_appends_to_file(temp_users_file):
    UsersRepo.add_user({"user_id": 1, "email": "a@test.com", "username": "alpha"})

    data = read_json(temp_users_file)
    assert len(data) == 1
    assert data[0]["user_id"] == 1

def test_update_user_changes_existing_user(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 3, "email": "old@test.com", "username": "old_name"}
    ]))

    updated = UsersRepo.update_user(3, {"email": "new@test.com"})
    assert updated["email"] == "new@test.com"

    data = read_json(temp_users_file)
    assert data[0]["email"] == "new@test.com"

def test_update_user_returns_none_if_not_found(temp_users_file):
    temp_users_file.write_text(json.dumps([]))
    assert UsersRepo.update_user(9, {"email": "missing@test.com"}) is None

def test_delete_user_removes_user(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 1}, {"user_id": 2}
    ]))

    result = UsersRepo.delete_user(1)
    assert result is True

    data = read_json(temp_users_file)
    assert data == [{"user_id": 2}]

def test_delete_user_returns_false_if_not_found(temp_users_file):
    temp_users_file.write_text(json.dumps([
        {"user_id": 99}
    ]))

    result = UsersRepo.delete_user(123)
    assert result is False
    assert read_json(temp_users_file) == [{"user_id": 99}]