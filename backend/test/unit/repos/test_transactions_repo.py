import json
import pytest
from pathlib import Path
from backend.app.repositories.transactions_repo import TransactionsRepo

@pytest.fixture
def temp_transactions_file(tmp_path, monkeypatch):
    temp = tmp_path / "transactions.json"
    temp.write_text("[]")

    monkeypatch.setattr(
        "backend.app.repositories.transactions_repo.DATA_PATH",
        temp
    )
    return temp


def read_json(path: Path):
    return json.loads(path.read_text())

def test_load_transactions_reads_file(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"user_id": 1, "type": "deposit", "amount": 100}
    ]))

    data = TransactionsRepo.load_transactions()
    assert data == [{"user_id": 1, "type": "deposit", "amount": 100}]

def test_get_transactions_by_user(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"transaction_id": "t1", "user_id": 1, "amount": 50},
        {"transaction_id": "t2", "user_id": 2, "amount": 20},
        {"transaction_id": "t3", "user_id": 1, "amount": 10},
    ]))

    result = TransactionsRepo.get_transactions_by_user(1)

    assert len(result) == 2
    assert all(t["user_id"] == 1 for t in result)

def test_save_transaction_overwrites_file(temp_transactions_file):
    TransactionsRepo.save_transaction([
        {"user_id": 5, "amount": 123}
    ])

    data = read_json(temp_transactions_file)
    assert data == [{"user_id": 5, "amount": 123}]

def test_add_transaction_appends_and_saves(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"transaction_id": "t1", "user_id": 1, "amount": 20}
    ]))

    new_tx = {"transaction_id": "t2", "user_id": 1, "amount": 30}

    result = TransactionsRepo.add_transaction(new_tx)
    assert result == new_tx

    saved = read_json(temp_transactions_file)
    assert saved == [
        {"transaction_id": "t1", "user_id": 1, "amount": 20},
        {"transaction_id": "t2", "user_id": 1, "amount": 30},
    ]

def test_transaction_exists_true(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"transaction_id": "abc123", "user_id": 1}
    ]))

    assert TransactionsRepo.transaction_exists("abc123") is True

def test_transaction_exists_false(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([]))

    assert TransactionsRepo.transaction_exists("missing") is False

def test_user_has_transactions_true(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"transaction_id": "t1", "user_id": 9}
    ]))

    assert TransactionsRepo.user_has_transactions(9) is True

def test_user_has_transactions_false(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([]))

    assert TransactionsRepo.user_has_transactions(1) is False