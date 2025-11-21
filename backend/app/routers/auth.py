from fastapi import APIRouter, HTTPException, status
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate, UserOut, ChangePassword
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter(prefix = "/auth", tags = ["Authentication"])


@router.post("/register", response_model = UserOut, status_code = status.HTTP_201_CREATED)
def register(payload: UserCreate):
    try:
        return AuthService().create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.post("/login", response_model = UserOut)
def login(payload: LoginRequest):
    user = AuthService().login(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code = 401, detail = "Incorrect email or password")
    return user

@router.patch("/change-password/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def change_password(user_id: int, payload: ChangePassword):
    AuthService().change_password(user_id, payload.old_password, payload.new_password)