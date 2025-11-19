from fastapi import APIRouter, Depends, HTTPException
from app.schemas.penalty import PenaltyCreate
from app.services.admin_service import AdminService
from app.services.users_service import get_user_info

router = APIRouter(prefix="/admin", tags=["Admin"])
service = AdminService()

def require_admin(user = Depends(get_user_info)):
    if not user.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.post("/promote/{user_id}")
def promote(user_id: int, admin = Depends(require_admin)):
    ok = service.promote_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": f"User {user_id} promoted to admin"}

@router.post("/penalty")
def penalty(data: PenaltyCreate, admin = Depends(require_admin)):
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

@router.get("/penalties/{user_id}")
def get_penalties(user_id: int, admin = Depends(require_admin)):
    return service.get_user_penalties(user_id)