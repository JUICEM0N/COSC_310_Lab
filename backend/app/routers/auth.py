from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate, UserOut, ChangePassword

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

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

@router.post("/login", response_model = UserOut, summary="User login")
def login(payload: LoginRequest):
    """
    This endpoint authenticates a user with the provided email and password.
    
    routers/auth.py -> services/auth_service.py/AuthService.login(email, password) -> 
    repositories/users_repo.py/UsersRepo.get_user_by_email(email)
    
    Args:
        payload (LoginRequest): The login credentials.
    Returns:
        UserOut: The authenticated user's details.
    """
    user = AuthService().login(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code = 401, detail = "Incorrect email or password")
    return user

@router.patch("/change-password/{user_id}", status_code = status.HTTP_204_NO_CONTENT, summary="Change user password")
def change_password(user_id: int, payload: ChangePassword):
    """
    This endpoint allows a user to change their password.
    
    routers/auth.py -> services/auth_service.py/AuthService.change_password(user_id, old_password, new_password) -> 
    repositories/users_repo.py/UsersRepo.change_password(user_id, new_password)

    Args:
        user_id (int): The ID of the user changing the password.
        payload (ChangePassword): The old and new passwords.
    Returns:
        None
    """
    AuthService().change_password(user_id, payload.old_password, payload.new_password)