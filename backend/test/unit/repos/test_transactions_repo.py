import json
import pytest
from pathlib import Path
from backend.app.repositories.transactions_repo import TransactionsRepo


@pytest.fixture
def temp_transactions_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "transactions.json"
    temp_file.write_text("[]")

    monkeypatch.setattr(
        "backend.app.repositories.transactions_repo.DATA_PATH",
        temp_file
    )
    return temp_file


def read_json(path: Path):
    return json.loads(path.read_text())


def test_load_transactions_reads_file(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"user_id": 1, "type": "deposit", "amount": 100}
    ]))

    transactions = TransactionsRepo.load_transactions()
    assert transactions == [{"user_id": 1, "type": "deposit", "amount": 100}]


def test_get_transactions_by_user(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"user_id": 1, "type": "deposit", "amount": 50},
        {"user_id": 2, "type": "withdraw", "amount": 25},
        {"user_id": 1, "type": "withdraw", "amount": 10},
    ]))

    result = TransactionsRepo.get_transactions_by_user(1)

    assert len(result) == 2
    assert all(t["user_id"] == 1 for t in result)


def test_save_transaction_overwrites_file(temp_transactions_file):
    TransactionsRepo.save_transaction([
        {"user_id": 3, "type": "deposit", "amount": 200}
    ])

    data = read_json(temp_transactions_file)
    assert data == [{"user_id": 3, "type": "deposit", "amount": 200}]


def test_add_transaction_appends_and_saves(temp_transactions_file):
    temp_transactions_file.write_text(json.dumps([
        {"user_id": 7, "type": "deposit", "amount": 10}
    ]))

    new_tx = {"user_id": 7, "type": "withdraw", "amount": 5}
    result = TransactionsRepo.add_transaction(new_tx)

    assert result == new_tx

    saved = read_json(temp_transactions_file)
    assert saved == [
        {"user_id": 7, "type": "deposit", "amount": 10},
        {"user_id": 7, "type": "withdraw", "amount": 5}
    ]
