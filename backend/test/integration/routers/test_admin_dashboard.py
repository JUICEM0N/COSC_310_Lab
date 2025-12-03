from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_admin_dashboard():
    response = client.get("/admin_dashboard/1")
    assert response.status_code == 200
    assert "message" in response.json()