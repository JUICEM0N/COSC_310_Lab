import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "penalties.json"

def get_penalties_by_user(user_id: int):
    with open(DATA_PATH) as file:
        penalties = json.load(file)
    return [p for p in penalties if p["user_id"] == user_id]