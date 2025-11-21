from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime
from typing import Optional
from backend.app.repositories.users_repo import UsersRepo
from backend.app.schemas.user import User, UserCreate

class AuthService:
    def create_user(self, user_data: UserCreate) -> User:
        if UsersRepo.get_user_by_email(user_data.email) or UsersRepo.get_user_by_username(user_data.username):
            raise ValueError("User already exists")
        
        hashed = hashpw(user_data.password.encode('utf-8'), gensalt()).decode('utf-8')

        new_user = User(
            user_id=len(UsersRepo.get_all_users()) + 1,
            username=user_data.username,
            password=hashed,
            email=user_data.email,
            isAdmin=user_data.isAdmin,
            createdAt=datetime.now().isoformat()
        )

        UsersRepo.add_user(new_user.model_dump())
        return new_user
    
    def login(self, email: str, password: str) -> Optional[User]:
        user_dict = UsersRepo.get_user_by_email(email)
        if user_dict and checkpw(password.encode('utf-8'), user_dict["password"].encode('utf-8')):
            return User(**user_dict)
        return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str):
        user_dict = UsersRepo.get_user_by_id(user_id)
        if not user_dict:
            raise ValueError("User not found")
        if not checkpw(old_password.encode('utf-8'), user_dict["password"].encode('utf-8')):
            raise ValueError("Incorrect password")
        new_hashed = hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')
        UsersRepo.update_user(user_id, {"password": new_hashed})

