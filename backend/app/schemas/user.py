from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: str
    password: str
    email: str
    isAdmin: bool = False
    createdAt: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    isAdmin: bool = False

class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    isAdmin: bool
    createdAt: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str
    password: str
    email: str
    isAdmin: bool

class ChangePassword(BaseModel):
    old_password: str
    new_password: str