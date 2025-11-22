from fastapi.testclient import TestClient
from backend.app.main import app
from datetime import datetime

client = TestClient(app)

def register_profile_user():
    timestamp = int(datetime.now().timestamp())
    username = f"profile_test_{timestamp}"
    email = f"profile{timestamp}@test.com"
    resp = client.post("/auth/register", json={
        "username": username,
        "password": "pass123",
        "email": email,
        "isAdmin": False
    })
    assert resp.status_code == 201
    return resp.json()["user_id"], timestamp

def test_get_and_update_profile():
    user_id, ts = register_profile_user()

    get_resp = client.get(f"/users/{user_id}/profile")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["username"].startswith("profile_test_")

    update_resp = client.put(f"/users/{user_id}/profile", json={
        "username": "jonah_updated",
        "email": f"updated{ts}@test.com",
        "password": "pass123",
        "isAdmin": False
    })
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["username"] == "jonah_updated"