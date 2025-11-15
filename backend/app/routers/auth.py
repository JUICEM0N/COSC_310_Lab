from fastapi import APIRouter, HTTPException, status
from services.auth_service import AuthService
from schemas.user import UserCreate, UserOut

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

@router.post("/register", response_model = UserOut, status_code = status.HTTP_201_CREATED)
def register(payload: UserCreate):
    try:
        return AuthService().create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.post("/login", response_model = UserOut)
def login(username: str, password: str):
    user = AuthService().login(username, password)
    if not user:
        raise HTTPException(status_code = 401, detail = "Incorrect email or password")
    return user