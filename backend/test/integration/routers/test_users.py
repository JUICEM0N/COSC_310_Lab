from fastapi.testclient import TestClient
from backend.app.main import app
import pytest

client = TestClient(app)

@pytest.mark.skip(reason="Users still in revision")
def test_get_profile():
    pass

@pytest.mark.skip(reason="Users still in revision")
def test_update_profile():
    pass

@pytest.mark.skip(reason="Users still in revision")
def test_change_password():
    pass