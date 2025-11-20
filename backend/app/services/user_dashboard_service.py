from backend.app.repositories.transactions_repo import TransactionsRepo
from backend.app.repositories.penalties_repo import PenaltiesRepo

class UserDashboardService:
    def get_user_dashboard(user_id: int):
        transactions = TransactionsRepo.get_transactions_by_user(user_id)
        penalties = PenaltiesRepo.get_penalties_by_user(user_id)

        transactions = sorted(transactions, key=lambda x: x.get("date", ""), reverse=True)

        return {
            "user_id": user_id,
            "transactions": transactions,
            "penalties": penalties
        }
