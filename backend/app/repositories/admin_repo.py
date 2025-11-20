import json
from pathlib import Path

DATA_DIR = Path("app/data")

class AdminRepository:
    def __init__(self):
        self.users_path = DATA_DIR / "users.json"
        self.penalties_path = DATA_DIR / "penalties.json"

    def load_users(self):
        with open(self.users_path, "r") as f:
            return json.load(f)

    def save_users(self, data):
        with open(self.users_path, "w") as f:
            json.dump(data, f, indent=2)

    def load_penalties(self):
        with open(self.penalties_path, "r") as f:
            return json.load(f)

    def save_penalties(self, data):
        with open(self.penalties_path, "w") as f:
            json.dump(data, f, indent=2)