import json
from pathlib import Path
from backend.app.repositories.cart_repo import CartRepo

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.json"

class UsersRepo:
    
    def load_users():
        if not DATA_PATH.exists():
            return []
        with open(DATA_PATH, "r") as f:
            return json.load(f)
        
    def save_users(users):
        with open(DATA_PATH, "w") as f:
            json.dump(users, f, indent=4)

    def get_all_users():
        return UsersRepo.load_users()

    def get_user_by_id(user_id: int):
        users = UsersRepo.load_users()
        for user in users:
            if user["user_id"] == user_id:
                return user
        return None

    def get_user_by_email(email: str):
        users = UsersRepo.load_users()
        for user in users:
            if user["email"] == email:
                return user
        return None

    def get_user_by_username(username: str):
        users = UsersRepo.load_users()
        for user in users:
            if user["username"] == username:
                return user
        return None

    def add_user(user_data: dict):
        # users = UsersRepo.load_users()
        # users.append(user_data)
        # UsersRepo.save_users(users)
        users = UsersRepo.load_users()

        users.append(user_data)
        UsersRepo.save_users(users)
        CartRepo.create_cart_for_user(user_data["user_id"])

    def update_user(user_id: int, updated_data: dict):
        users = UsersRepo.load_users()
        for i, user in enumerate(users):
            if user["user_id"] == user_id:
                users[i].update(updated_data)
                UsersRepo.save_users(users)
                return users[i]
        return None

    def delete_user(user_id: int):
        users = UsersRepo.load_users()
        new_users = [u for u in users if u["user_id"] != user_id]
        UsersRepo.save_users(new_users)
        return len(new_users) < len(users)

    def user_exists(user_id: int) -> bool:
        users = UsersRepo.load_users()
        return any(user["user_id"] == user_id for user in users)