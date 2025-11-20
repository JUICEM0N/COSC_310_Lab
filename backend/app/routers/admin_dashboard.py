from fastapi import APIRouter, Depends, HTTPException
from app.services.admin_service import AdminService
from app.services.users_service import get_user_info
from app.repositories.users_repo import load_users
from app.repositories.transactions_repo import get_transactions_by_user
from app.repositories.penalties_repo import get_penalties_by_user

router = APIRouter(prefix="/admin_dashboard", tags=["Admin Dashboard"])
service = AdminService()
#requires admin
def require_admin(user=Depends(get_user_info)):
    if not user.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

#gets a overview of all users
@router.get("/users")
def get_all_users(admin=Depends(require_admin)):
    users = load_users()
    if not users:
        return {"message": "No users found"}
    return {
        "message": "All users retrieved successfully",
        "users": users
    }

#gets the dashboard of a specific user
@router.get("/user/{user_id}")
def get_user_details(user_id: int, admin=Depends(require_admin)):
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = get_transactions_by_user(user_id)
    penalties = get_penalties_by_user(user_id)

    return {
        "message": f"Dashboard for user {user_id}",
        "user": user,
        "transactions": transactions,
        "penalties": penalties
    }


@router.get("/summary")
def admin_summary(admin=Depends(require_admin)):
    users = load_users()

    #gather global data
    all_transactions = []
    all_penalties = []

    for user in users:
        uid = user["id"]
        all_transactions.extend(get_transactions_by_user(uid))
        all_penalties.extend(get_penalties_by_user(uid))

    #sort latest items
    all_transactions_sorted = sorted(
        all_transactions,
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    all_penalties_sorted = sorted(
        all_penalties,
        key=lambda x: x.get("date_issued", ""),
        reverse=True
    )

    return {
        "message": "Admin dashboard summary",
        "totals": {
            "total_users": len(users),
            "total_transactions": len(all_transactions),
            "total_penalties": len(all_penalties)
        },
        "latest": {
            "recent_transactions": all_transactions_sorted[:10],
            "recent_penalties": all_penalties_sorted[:10]
        }
    }