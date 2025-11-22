import json, os
from pathlib import Path
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "amazon_cad.json"

class ProductsRepo:
    
    def load_products():
        with open(DATA_PATH, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
        
    def get_products(product_id: str):
        return next((p for p in ProductsRepo.load_products() if p["product_id"] == product_id), None)
    
    # Functions from FastAPI Demo
    @staticmethod
    def load_all():
        with open(DATA_PATH, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)

    def save_all(items: List[Dict[str, Any]]) -> None:
        tmp = DATA_PATH.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_PATH)

    def product_exists(product_id: str) -> bool:
        items = ProductsRepo.load_all()
        return any(item["product_id"] == product_id for item in items)