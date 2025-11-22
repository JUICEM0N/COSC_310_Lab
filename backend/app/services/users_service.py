from backend.app.repositories.users_repo import UsersRepo
from bcrypt import checkpw, hashpw, gensalt

class UsersService:
    @staticmethod
    def get_user_info(user_id: int):
        return UsersRepo.get_user_by_id(user_id)

    @staticmethod
    def update_user(user_id: int, updated_data: dict):
        users = UsersRepo.load_users()
        user = next((u for u in users if u["user_id"] == user_id), None)
        if not user:
            return None
        user.update(updated_data)
        UsersRepo.save_users(users)
        return user

    @staticmethod
    def change_user_password(user_id: int, old_password: str, new_password: str) -> bool:
        user = UsersRepo.get_user_by_id(user_id)
        if not user:
            return False

        if not checkpw(old_password.encode('utf-8'), user["password"].encode('utf-8')):
            return False

        new_hashed = hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')
        user["password"] = new_hashed

        users = UsersRepo.load_users()
        for i, u in enumerate(users):
            if u["user_id"] == user_id:
                users[i] = user
                break
        UsersRepo.save_users(users)
        return True