from fastapi import Depends, HTTPException, Header
from jose import JWTError, jwt
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
from backend.app.repositories.users_repo import UsersRepo  

env_path = Path(__file__).resolve().parent.parent / "totally_not_private_keys.env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set"
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int):
    """Generate a JWT token for a user"""
    expire = int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {"user_id": user_id, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(authorization: str = Header(None, alias="Authorization")):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = UsersRepo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")