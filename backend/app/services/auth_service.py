from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime
from repositories.users_repo import *
from schemas.user import User, UserCreate
from typing import Optional

class AuthService:
    def create_user(self, user_data: UserCreate) -> User:
        if get_user_by_email(user_data.email) or get_user_by_username(user_data.username):
            raise ValueError("User already exists")
        
        hashed = hashpw(user_data.password.encode('utf-8'), gensalt()).decode('utf-8')

        new_user = User(
            user_id=len(get_all_users()) + 1,
            username=user_data.username,
            password=hashed,
            email=user_data.email,
            isAdmin=user_data.isAdmin,
            createdAt=datetime.now()
        )

        add_user(new_user.model_dump())
        return new_user
    
    def login(self, email: str, password: str) -> Optional[User]:
        user_dict = get_user_by_email(email)
        if user_dict and checkpw(password.encode('utf-8'), user_dict["password"].encode('utf-8')):
            return User(**user_dict)
        return None