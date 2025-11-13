from fastapi import APIRouter, HTTPException
from schemas.user import User, UserUpdate, ChangePassword
from services.users_service import get_user_by_id, update_user, change_user_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/profile", response_model=User)
def get_profile(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/profile", response_model=User)
def put_profile(user_id: str, payload: UserUpdate):
    updated_user = update_user(user_id, payload)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.post("/{user_id}/change-password", status_code=204)
def post_change_password(user_id: str, payload: ChangePassword):
    success = change_user_password(user_id, payload.old_password, payload.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Password change failed")
    return None