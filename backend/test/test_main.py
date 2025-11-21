from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}

# def test_health():
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200