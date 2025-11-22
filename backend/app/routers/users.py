from fastapi import APIRouter, HTTPException
from backend.app.schemas.user import User, UserUpdate, ChangePassword
from backend.app.services.users_service import UsersService
from backend.app.repositories.users_repo import UsersRepo

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/get/{user_id}/profile", response_model=User, summary="Get user profile by user ID")
def get_profile(user_id: int):
    """
    This endpoint gets the user profile by user_id.

    routers/users.py -> repositories/users_repo.py

    Args:
        user_id (int): The ID of the user.
    Returns:
        User: The user profile data.
    """
    user = UsersRepo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/update/{user_id}/profile", response_model=User, summary="Update user profile by user ID")
def put_profile(user_id: str, payload: UserUpdate):
    """
    This endpoint updates the user profile by user_id.

    routers/users.py -> services/users_service.py/UsersService.update_user(user_id, payload)
    routers/users.py -> services/users_service.py/UsersService.update_user(user_id, payload) 
    -> repositories/users_repo.py/UsersRepo.load_users()
    routers/users.py -> services/users_service.py/UsersService.update_user(user_id, payload) 
    -> repositories/users_repo.py/UsersRepo.save_users(users)

    Args:
        user_id (str): The ID of the user.
        payload (UserUpdate): The updated user data.
    Returns:
        User: The updated user profile data.
    """
    updated_user = UsersService.update_user(user_id, payload)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.post("/{user_id}/change-password", status_code=204, summary="Changes the password for a user")
def post_change_password(user_id: str, payload: ChangePassword):
    """
    This endpoint changes the password for a user.

    routers/users.py -> services/users_service.py/UsersService.change_user_password(user_id, old_password, new_password) 
    -> repositoriess/users_repo.py/UsersRepo.load_users()
    routers/users.py -> services/users_service.py/UsersService.change_user_password(user_id, old_password, new_password) 
    -> repositoriess/users_repo.py/UsersRepo.save_users(users)
    
    Args:
        user_id (str): The ID of the user.
        payload (ChangePassword): The old and new password data.
    Returns:
        None
    """
    success = UsersService.change_user_password(user_id, payload.old_password, payload.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Password change failed")
    return None