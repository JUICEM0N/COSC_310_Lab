from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_user_dashboard():
    response = client.get("/user_dashboard/1")
    assert response.status_code == 200
    assert "message" in response.json()
