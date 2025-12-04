from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate, UserOut, ChangePassword
from backend.app.utils.auth import get_current_user

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    user: UserOut

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

@router.post("/change-password", summary="Change user password")
def change_password(payload: ChangePassword, current_user: dict = Depends(get_current_user)):
    """
    This endpoint allows an authenticated user to change their password.
    
    routers/auth.py -> services/auth_service.py/AuthService.change_password(user_id, old_password, new_password)
    
    Args:
        payload (ChangePassword): The old and new password.
        current_user (dict): The authenticated user.
    Returns:
        dict: Success message.
    """
    try:
        AuthService().change_password(current_user["user_id"], payload.old_password, payload.new_password)
        return {"msg": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/register", response_model = UserOut, status_code = status.HTTP_201_CREATED, summary="Register a new user")
def register(payload: UserCreate):
    """
    This endpoint registers a new user with the provided details (payload).

    routers/auth.py -> services/auth_service.py/AuthService.create_user(payload) -> 
    repositories/users_repo.py/UsersRepo.create_user(payload)

    Args:
        payload (UserCreate): The user details for registration.
    Returns:
        UserOut: The created user's details.
    """
    try:
        return AuthService().create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.post("/login", response_model = LoginResponse, summary="User login")
def login(payload: LoginRequest):
    """
    This endpoint authenticates a user with the provided email and password.
    
    routers/auth.py -> services/auth_service.py/AuthService.login(email, password) -> 
    repositories/users_repo.py/UsersRepo.get_user_by_email(email)
    
    Args:
        payload (LoginRequest): The login credentials.
    Returns:
        LoginResponse: The authenticated user's details and JWT access token.
    """
    result = AuthService().login(payload.email, payload.password)
    if not result:
        raise HTTPException(status_code = 401, detail = "Incorrect email or password")
    return {"access_token": result["access_token"], "user": result["user"]}
   

