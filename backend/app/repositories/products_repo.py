import json, os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import HTTPException

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
    
    def search_products(keyword: str):
        products = ProductsRepo.load_products()
        k = keyword.lower()

        results = [p for p in products if k in p.get("product_name", "").lower()]

        if not results:
            raise HTTPException(status_code=404, detail=f"Looks like we don\'t have {keyword}, sorry :(")

        return results
    
    def filter_products(keyword=None, min_price=None, max_price=None,
                    category=None, rating=None):

        products = ProductsRepo.load_products()
        results = products

        if keyword:
            k = keyword.lower()
            results = [
                p for p in results
                if k in p.get("product_name", "").lower()
            ]

        def parse_price(price_str):
            try:
                return float(price_str.replace("$", "").replace(",", ""))
            except:
                return None
            
        def parse_rating(r):
            try:
                cleaned = str(r).replace("|", "").strip()
                if cleaned == "":
                    return None
                return float(cleaned)
            except:
                return None

        if min_price is not None:
            results = [
                p for p in results
                if parse_price(p.get("discounted_price")) is not None and
                    parse_price(p.get("discounted_price")) >= min_price
            ]

        if max_price is not None:
            results = [
                p for p in results
                if parse_price(p.get("discounted_price")) is not None and
                    parse_price(p.get("discounted_price")) <= max_price
            ]

        if category:
            c = category.lower()
            results = [
                p for p in results
                if c in p.get("category", "").lower()
            ]

        if rating is not None:
            results = [
                p for p in results
                if parse_rating(p.get("rating")) is not None and parse_rating(p.get("rating")) >= rating]

        if not results:
            raise HTTPException(status_code=404, detail="No products found matching the filter criteria.")

        return results