import json
from pathlib import Path
import uuid

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions.json"

class TransactionsRepo:

    @staticmethod
    def get_transactions_by_user(user_id: int):
        transactions = TransactionsRepo.load_transactions()
        return [t for t in transactions if t["user_id"] == user_id]
    
    @staticmethod
    def load_transactions():
        with open(DATA_PATH, "r") as f:
            return json.load(f)
        
    @staticmethod
    def save_transaction(transactions):
            with open(DATA_PATH, "w") as f:
                json.dump(transactions, f, indent=4)

    @staticmethod
    def add_transaction(data: dict) -> dict:
        if "transaction_id" not in data:
            data["transaction_id"] = str(uuid.uuid4())
        transactions = TransactionsRepo.load_transactions()
        transactions.append(data)
        TransactionsRepo.save_transaction(transactions)
        return data
    
    @staticmethod
    def transaction_exists(transaction_id: str) -> bool:
        return any(t.get("transaction_id") == transaction_id for t in TransactionsRepo.load_transactions())
        
    @staticmethod
    def user_has_transactions(user_id: int) -> bool:
        transactions = TransactionsRepo.load_transactions()
        return any(t.get("user_id") == user_id for t in transactions)

    @staticmethod
    def get_transaction_by_id(transaction_id: str) -> dict | None:
        transactions = TransactionsRepo.load_transactions()
        return next((t for t in transactions if t.get("transaction_id") == transaction_id), None)

    @staticmethod
    def get_transaction_by_intent(intent_id: str) -> dict | None:
        transactions = TransactionsRepo.load_transactions()
        return next((t for t in transactions if t.get("payment_intent_id") == intent_id), None)

    @staticmethod
    def update_transaction(transaction_id: str, updates: dict) -> dict | None:
        transactions = TransactionsRepo.load_transactions()
        for t in transactions:
            if t.get("transaction_id") == transaction_id:
                t.update(updates)
                TransactionsRepo.save_transaction(transactions)
                return t
        return None
