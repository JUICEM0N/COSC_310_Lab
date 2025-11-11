from repositories.users_repo import get_user_by_id, load_users, save_users

def get_user_info(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        return None
    return user

def update_user(user_id, updated_data):
    users = load_users()

    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return None

    for key, value in updated_data.items():
        if key in user:
            user[key] = value

    save_users(users)
    return user

def change_user_password(user_id, old_password, new_password):
    users = load_users()

    user = next((u for u in users if u["id"] == user_id), None)
    if not user or user.get("password") != old_password:
        return False

    user["password"] = new_password
    save_users(users)
    return True