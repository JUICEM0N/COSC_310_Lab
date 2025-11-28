from fastapi import APIRouter, Depends, HTTPException
from backend.app.services.admin_service import AdminService
from backend.app.services.users_service import UsersService
from backend.app.repositories.users_repo import UsersRepo
from backend.app.repositories.transactions_repo import TransactionsRepo
from backend.app.repositories.penalties_repo import PenaltiesRepo

router = APIRouter(prefix="/admin_dashboard", tags=["Admin Dashboard"])
service = AdminService()

#requires admin
def require_admin(user=Depends(UsersService.get_user_info)):
    if not user.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

#gets a overview of all users
@router.get("/users", summary="Get all users")
def get_all_users(admin=Depends(require_admin)):
    """
    This endpoint retrieves all users in the system. Admin access is required.
    
    routers/admin_dashboard.py -> repositories/users_repo.py/UsersRepo.load_users()
    
    Args:
        admin: The admin user making the request.
    Returns:
        dict: A dictionary containing a message and the list of users.
    """
    users = UsersRepo.load_users()
    if not users:
        return {"message": "No users found"}
    return {
        "message": "All users retrieved successfully",
        "users": users
    }

#gets the dashboard of a specific user
@router.get("/user/{user_id}", summary="Get user dashboard")
def get_user_details(user_id: int, admin=Depends(require_admin)):
    """
    This endpoint retrieves the dashboard details of a specific user by their ID. Admin access is required.
    
    routers/admin_dashboard.py -> repositories/users_repo.py/UsersRepo.load_users()
    
    routers/admin_dashboard.py -> repositories/transactions_repo.py/TransactionsRepo.get_transactions_by_user(user_id)
    
    routers/admin_dashboard.py -> repositories/penalties_repo.py/PenaltiesRepo.get_penalties(user_id)
    
    Args:
        user_id (int): The ID of the user whose dashboard is to be retrieved.
        admin: The admin user making the request.
    Returns:
        dict: A dictionary containing the user's dashboard details.
    """
    users = UsersRepo.load_users()
    user = next((u for u in users if u["user_id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = TransactionsRepo.get_transactions_by_user(user_id)
    penalties = PenaltiesRepo.get_penalties_by_user(user_id)

    return {
        "message": f"Dashboard for user {user_id}",
        "user": user,
        "transactions": transactions,
        "penalties": penalties
    }

# summary
@router.get("/summary", summary="Get admin dashboard summary")
def admin_summary(admin=Depends(require_admin)):
    """
    This endpoint retrieves a summary for the admin dashboard, including total counts and recent activities.
    
    routers/admin_dashboard.py -> repositories/users_repo.py/UsersRepo.load_users()
    routers/admin_dashboard.py -> repositories/transactions_repo.py/TransactionsRepo.get_transactions_by_user(user_id)
    routers/admin_dashboard.py -> repositories/penalties_repo.py/PenaltiesRepo.get_penalties
    
    Args:
        admin: The admin user making the request.
    Returns:
        dict: A dictionary containing summary statistics and recent activities.
    """
    users = UsersRepo.load_users()

    all_transactions = []
    all_penalties = []

    for user in users:
        uid = user["user_id"]
        all_transactions.extend(TransactionsRepo.get_transactions_by_user(uid))
        all_penalties.extend(PenaltiesRepo.get_penalties_by_user(uid))

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
