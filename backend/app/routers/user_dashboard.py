from fastapi import APIRouter, HTTPException
from backend.app.services.user_dashboard_service import UserDashboardService

router = APIRouter(prefix="/user_dashboard", tags=["User Dashboard"])

""" Gets dashboard info for a specific user based on user_id"""
@router.get("/{user_id}")
def get_dashboard(user_id: int):
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