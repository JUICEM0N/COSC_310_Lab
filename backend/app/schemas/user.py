from pydantic import BaseModel, StrictBool
from typing import Optional
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: str
    password: str
    email: str
    isAdmin: StrictBool = False
    createdAt: str = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    isAdmin: StrictBool = False

class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    isAdmin: StrictBool
    createdAt: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str
    email: str
    isAdmin: StrictBool

class ChangePassword(BaseModel):
    old_password: str
    new_password: str