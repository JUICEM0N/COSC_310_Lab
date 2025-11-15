# Uncomment below when testing with PyTest
# from backend.app.repositories.transactions_repo import get_transactions_by_user
# from backend.app.repositories.penalties_repo import get_penalties_by_user

# Uncomment below when running FastAPI
from repositories.transactions_repo import TransactionsRepo
from repositories.penalties_repo import get_penalties_by_user

def get_user_dashboard(user_id: int):
    transactions = TransactionsRepo.get_transactions_by_user(user_id)
    penalties = get_penalties_by_user(user_id)

    transactions = sorted(transactions, key=lambda x: x.get("date", ""), reverse=True)

    return {
        "user_id": user_id,
        "transactions": transactions,
        "penalties": penalties
    }
