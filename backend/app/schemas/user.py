from pydantic import BaseModel
import datetime

class User(BaseModel):
    user_id: int
    username: str
    password: str
    email: str
    isAdmin: bool
    createdAt: datetime.datetime

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    isAdmin: bool

class UserUpdate(BaseModel):
    username: str
    password: str
    email: str
    isAdmin: bool

class ChangePassword(BaseModel):
    old_password: str
    new_password: str