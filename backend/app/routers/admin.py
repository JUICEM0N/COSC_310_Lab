from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.penalty import PenaltyCreate
from backend.app.services.admin_service import AdminService
from backend.app.services.users_service import UsersService

router = APIRouter(prefix="/admin", tags=["Admin"])
service = AdminService()

def require_admin(user = Depends(UsersService.get_user_info)):
    if not user or not isinstance(user, dict):
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not user.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.post("/promote/{user_id}", summary="Promote a user to admin")
def promote(user_id: int, admin = Depends(require_admin)):
    """
    This endpoints changes a users isAdmin from False to True.

    routers/admin.py -> services/admin_service.py/AdminService.promote_user(user_id) 

    Args:
        user_id (int): The ID of the user to promote.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success or failure.
    """
    ok = service.promote_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": f"User {user_id} promoted to admin"}

@router.post("/penalty", summary="Apply a penalty to a user")
def penalty(data: PenaltyCreate, admin = Depends(require_admin)):
    """
    This endpoint applies a penalty to a user.

    routers/admin.py -> services/admin_service.py/AdminService.apply_penalty(data)

    Args:
        data (PenaltyCreate): The penalty data.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success and the penalty ID.
    """
    pid = service.apply_penalty(
        data.user_id,
        data.reason,
        data.amount,
        data.status
    )
    return {
        "msg": "Penalty applied",
        "penalty_id": pid
    }

@router.get("/penalties/{user_id}", summary="Get penalties for a user")
def get_penalties(user_id: int, admin = Depends(require_admin)):
    """
    This endpoint retrieves all penalties for a specific user.
    
    routers/admin.py -> services/admin_service.py/AdminService.get_user_penalties(user_id)
    
    Args:
        user_id (int): The ID of the user whose penalties are to be retrieved.
        admin: The current admin user (injected by dependency).
    Returns:
        list: A list of penalties for the user."""
    return service.get_user_penalties(user_id)