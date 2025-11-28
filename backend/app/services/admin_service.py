import uuid
from datetime import datetime
from backend.app.repositories.admin_repo import AdminRepository

repo = AdminRepository()

class AdminService:

    def promote_user(self, user_id: int):
        users = repo.load_users()

        for user in users:
            if user["user_id"] == user_id:
                user["isAdmin"] = True
                repo.save_users(users)
                return True

        return False

    def apply_penalty(self, user_id: int, reason: str, amount: float, status: str):
        penalties = repo.load_penalties()
        penalty_id = str(uuid.uuid4())

        new_penalty = {
            "id": penalty_id,
            "user_id": user_id,
            "reason": reason,
            "amount": amount,
            "status": status,
            "date_issued": datetime.utcnow().isoformat()
        }

        penalties.append(new_penalty)
        repo.save_penalties(penalties)

        return penalty_id

    def get_user_penalties(self, user_id: int):
        penalties = repo.load_penalties()
        return [p for p in penalties if p["user_id"] == user_id]