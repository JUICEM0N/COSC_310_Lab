import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions.json"

class TransactionsRepo:

    def get_transactions_by_user(user_id: int):
        transactions = TransactionsRepo.load_transactions()
        return [t for t in transactions if t["user_id"] == user_id]
    
    def load_transactions():
        with open(DATA_PATH, "r") as f:
            return json.load(f)
        
    def save_transaction(transactions):
            with open(DATA_PATH, "w") as f:
                json.dump(transactions, f, indent=4)

    def add_transaction(data):
        transactions = TransactionsRepo.load_transactions()
        transactions.append(data)
        TransactionsRepo.save_transaction(transactions)
        return data