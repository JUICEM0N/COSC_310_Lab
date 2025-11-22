from fastapi import APIRouter, HTTPException
from backend.app.services.user_dashboard_service import UserDashboardService

router = APIRouter(prefix="/user_dashboard", tags=["User Dashboard"])

@router.get("/{user_id}", summary="Get User Dashboard Info")
def get_dashboard(user_id: int):
    """ 
    This endpoint gets dashboard info for a specific user based on user_id. This shows the users
    recent transactions and any penalties they may have incurred.

    routers/user_dashboard.py -> services/user_dashboard_service.py/UserDashboardService.get_user_dashboard()
    routers/user_dashboard.py -> repositories/transactions_repo.py/TransactionsRepo.get_transactions_by_user(user_id)
    routers/user_dashboard.py -> repositories/penalties_repo.py/PenaltiesRepo.get_penalties_by_user(user_id)   
    
    Args:
        user_id (int): The ID of the user whose dashboard info is to be retrieved.
    Returns:
        dict: A dictionary containing the user's dashboard information, including
            recent transactions and penalties.
    """
    try:
        dashboard_data = UserDashboardService.get_user_dashboard(user_id)
        if not dashboard_data["transactions"] and not dashboard_data["penalties"]:
            return {"message": f"No data found for user {user_id}"}
        return {
            "message": "User dashboard retrieved successfully",
            "data": dashboard_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))