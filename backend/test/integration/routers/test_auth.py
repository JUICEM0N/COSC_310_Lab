from fastapi.testclient import TestClient
from backend.app.main import app
from datetime import datetime

client = TestClient(app)

def test_register_and_login_full_flow():
    timestamp = int(datetime.now().timestamp())
    username = f"jonah_test_{timestamp}"
    email = f"jonah{timestamp}@test.com"

    reg_resp = client.post("/auth/register", json={
        "username": username,
        "password": "secure123",
        "email": email,
        "isAdmin": False
    })
    assert reg_resp.status_code == 201
    user_id = reg_resp.json()["user_id"]

    login_resp = client.post("/auth/login", json={
        "email": email,
        "password": "secure123"
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["username"] == username

    change_resp = client.patch(f"/auth/change-password/{user_id}", json={
        "old_password": "secure123",
        "new_password": "newsecure456"
    })
    assert change_resp.status_code == 204

    new_login = client.post("/auth/login", json={
        "email": email,
        "password": "newsecure456"
    })
    assert new_login.status_code == 200

    wrong_resp = client.patch(f"/auth/change-password/{user_id}", json={
        "old_password": "wrong",
        "new_password": "fail"
    })
    assert wrong_resp.status_code == 400