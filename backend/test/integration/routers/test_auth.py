from backend.app.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

@pytest.mark.skip(reason="Auth still in revision")
def test_register_user():
    pass

@pytest.mark.skip(reason="Auth still in revision")
def test_login_invalid_credentials():
    pass
