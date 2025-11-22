import json
from pathlib import Path
from backend.app.repositories.admin_repo import AdminRepository

def make_temp_repo(tmp_path):
    users_path = tmp_path / "users.json"
    penalties_path = tmp_path / "penalties.json"

    users_path.write_text("[]")
    penalties_path.write_text("[]")   

    repo = AdminRepository()

    repo.users_path = users_path
    repo.penalties_path = penalties_path

    return repo


def test_load_users(tmp_path):
    repo = make_temp_repo(tmp_path)

    users = repo.load_users()
    assert isinstance(users, list)
    assert users == []


def test_save_users(tmp_path):
    repo = make_temp_repo(tmp_path)

    data = [{"id": 1, "name": "Alice"}]
    repo.save_users(data)

    saved = json.loads(repo.users_path.read_text())
    assert saved == data


def test_load_penalties(tmp_path):
    repo = make_temp_repo(tmp_path)

    penalties = repo.load_penalties()
    assert isinstance(penalties, list)
    assert penalties == []


def test_save_penalties(tmp_path):
    repo = make_temp_repo(tmp_path)

    data = [{"id": "123", "user_id": 1, "amount": 50}]
    repo.save_penalties(data)

    saved = json.loads(repo.penalties_path.read_text())
    assert saved == data
