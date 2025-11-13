import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions.json"

def get_transactions_by_user(user_id: int):
    with open(DATA_PATH) as file:
        transactions = json.load(file)
    return [t for t in transactions if t["user_id"] == user_id]