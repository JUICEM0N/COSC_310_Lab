import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.json"

def load_users():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)
    
def save_users(users):
    with open(DATA_PATH, "w") as f:
        json.dump(users, f, indent=4)

def get_all_users():
    return load_users()

def get_user_by_id(user_id: int):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def get_user_by_email(email: str):
    users = load_users()
    for user in users:
        if user["email"] == email:
            return user
    return None

def add_user(user_data: dict):
    users = load_users()
    users.append(user_data)
    save_users(users)

def update_user(user_id: int, updated_data: dict):
    users = load_users()
    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i].update(updated_data)
            save_users(users)
            return users[i]
    return None

def delete_user(user_id: int):
    users = load_users()
    new_users = [u for u in users if u["id"] != user_id]
    save_users(new_users)
    return len(new_users) < len(users)