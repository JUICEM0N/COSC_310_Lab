import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "amazon_cad.json"

class ProductsRepo:
    
    def load_products():
        with open(DATA_PATH, "r") as f:
            return json.load(f)
        
    def get_product(product_id: str):
        products = ProductsRepo.load_products()
        return next((p for p in products if p["product_id"] == product_id), None)