import pytest
from datetime import datetime
from pydantic import ValidationError
from backend.app.schemas.transaction import Transaction, TransactionCreate


def valid_transaction():
    return {
        "transaction_id": 1,
        "user_id": 1,
        "amount": 50.0,
        "timestamp": datetime(2025, 1, 1, 12, 0, 0)
    }

def valid_create_data():
    return {
        "user_id": 1,
        "amount": 50.0
    }

def test_transaction_valid():
    t = Transaction(**valid_transaction())
    assert t.transaction_id == 1
    assert t.user_id == 1
    assert t.amount == 50.0
    assert isinstance(t.timestamp, datetime)


def test_transaction_accepts_datetime_string():
    data = valid_transaction()
    data["timestamp"] = "2025-01-01T12:00:00"
    t = Transaction(**data)
    assert isinstance(t.timestamp, datetime)

def test_transaction_missing_field():
    data = valid_transaction()
    data.pop("timestamp")
    with pytest.raises(ValidationError):
        Transaction(**data)

def test_transaction_invalid_amount_type():
    data = valid_transaction()
    data["amount"] = "not-a-number"
    with pytest.raises(ValidationError):
        Transaction(**data)

def test_transaction_create_valid():
    t = TransactionCreate(**valid_create_data())
    assert t.user_id == 1
    assert t.amount == 50.0

def test_transaction_create_missing_amount():
    data = valid_create_data()
    data.pop("amount")
    with pytest.raises(ValidationError):
        TransactionCreate(**data)

def test_transaction_create_invalid_type():
    data = valid_create_data()
    data["amount"] = "abc"
    with pytest.raises(ValidationError):
        TransactionCreate(**data)

def test_transaction_create_allows_float_string():
    data = valid_create_data()
    data["amount"] = "25.5"
    t = TransactionCreate(**data)
    assert t.amount == 25.5