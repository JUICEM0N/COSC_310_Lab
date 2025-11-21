import pytest
from datetime import datetime
from pydantic import ValidationError
from backend.app.schemas.penalty import Penalty, PenaltyCreate, PenaltyUpdate

def valid_penalty_data():
    return {
        "id": "p1",
        "user_id": 1,
        "reason": "Late payment",
        "amount": 25.5,
        "status": "unpaid",
        "date_issued": datetime(2025, 1, 1, 12, 0, 0)
    }

def valid_create_data():
    d = valid_penalty_data()
    d.pop("id")
    d.pop("date_issued")
    return d

def test_penalty_valid():
    p = Penalty(**valid_penalty_data())
    assert p.user_id == 1
    assert p.amount == 25.5
    assert isinstance(p.date_issued, datetime)

def test_penalty_missing_date_issued():
    data = valid_penalty_data()
    data.pop("date_issued")
    with pytest.raises(ValidationError):
        Penalty(**data)

def test_penalty_invalid_amount_type():
    data = valid_penalty_data()
    data["amount"] = "twenty"
    with pytest.raises(ValidationError):
        Penalty(**data)

def test_penalty_datetime_string_parses():
    data = valid_penalty_data()
    data["date_issued"] = "2025-01-01T12:00:00"
    p = Penalty(**data)
    assert isinstance(p.date_issued, datetime)

def test_penalty_create_valid():
    data = valid_create_data()
    p = PenaltyCreate(**data)
    assert p.status == "unpaid"

def test_penalty_create_missing_required_field():
    data = valid_create_data()
    data.pop("reason")
    with pytest.raises(ValidationError):
        PenaltyCreate(**data)

def test_penalty_create_invalid_type():
    data = valid_create_data()
    data["amount"] = "25.5"
    assert isinstance(PenaltyCreate(**data).amount, float)


def test_penalty_update_valid():
    p = PenaltyUpdate(reason="Updated", amount=10.0, status="paid")
    assert p.reason == "Updated"
    assert p.status == "paid"

def test_penalty_update_missing_field():
    with pytest.raises(ValidationError):
        PenaltyUpdate(amount=10.0, status="paid") 


def test_penalty_update_invalid_amount_type():
    with pytest.raises(ValidationError):
        PenaltyUpdate(reason="Test", amount="notfloat", status="unpaid")
