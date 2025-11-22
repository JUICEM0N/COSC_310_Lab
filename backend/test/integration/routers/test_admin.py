from fastapi.testclient import TestClient
from backend.app.main import app
import pytest

client = TestClient(app)


@pytest.mark.skip(reason="Admin router still in revision")
def test_promote_user():
    pass


@pytest.mark.skip(reason="Admin router still in revision")
def test_apply_penalty():
    pass


@pytest.mark.skip(reason="Admin router still in revision")
def test_get_penalties():
    pass