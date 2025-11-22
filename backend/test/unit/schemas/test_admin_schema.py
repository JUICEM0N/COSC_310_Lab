import pytest
from pydantic import ValidationError
from backend.app.schemas.admin import PromoteUser, ApplyPenalty


def test_promote_user_valid():
    data = {"user_id": 5}
    obj = PromoteUser(**data)
    assert obj.user_id == 5


def test_promote_user_invalid_missing_field():
    with pytest.raises(ValidationError):
        PromoteUser()


def test_promote_user_invalid_type():
    with pytest.raises(ValidationError):
        PromoteUser(user_id="abc")


def test_apply_penalty_valid():
    data = {
        "user_id": 10,
        "reason": "Late payment",
        "amount": 25.5,
        "status": "pending"
    }

    obj = ApplyPenalty(**data)

    assert obj.user_id == 10
    assert obj.reason == "Late payment"
    assert obj.amount == 25.5
    assert obj.status == "pending"


def test_apply_penalty_missing_field():
    with pytest.raises(ValidationError):
        ApplyPenalty(
            user_id=10,
            reason="Late payment",
            amount=20.0
        )


def test_apply_penalty_invalid_amount_type():
    with pytest.raises(ValidationError):
        ApplyPenalty(
            user_id=10,
            reason="Test",
            amount="twenty",
            status="pending"
        )


def test_apply_penalty_invalid_user_id_type():
    with pytest.raises(ValidationError):
        ApplyPenalty(
            user_id="xyz",
            reason="Test",
            amount=5,
            status="ok"
        )
