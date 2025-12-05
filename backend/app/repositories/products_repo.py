import json, os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import HTTPException

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "amazon_cad.json"
POW_PATH = DATA_PATH.with_name("products_of_week.json")
DISCOUNTS_PATH = DATA_PATH.with_name("discounts.json")

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

    #product of the week
    @staticmethod
    def _ensure_pow_exists():
        if not POW_PATH.exists():
            with open(POW_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
    #allows for mutiple products of the week
    @staticmethod
    def set_products_of_the_week(product_ids: List[str]) -> None:
        ProductsRepo._ensure_pow_exists()
        tmp = POW_PATH.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(product_ids, f, indent=2)
        os.replace(tmp, POW_PATH)

    @staticmethod
    def get_products_of_the_week() -> List[str]:
        ProductsRepo._ensure_pow_exists()
        with open(POW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    #discounts
    @staticmethod
    def _ensure_discounts_exists():
        if not DISCOUNTS_PATH.exists():
            with open(DISCOUNTS_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    @staticmethod
    def load_discounts() -> List[Dict[str, Any]]:
        ProductsRepo._ensure_discounts_exists()
        with open(DISCOUNTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_discounts(discounts: List[Dict[str, Any]]) -> None:
        ProductsRepo._ensure_discounts_exists()
        tmp = DISCOUNTS_PATH.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(discounts, f, indent=2)
        os.replace(tmp, DISCOUNTS_PATH)

    @staticmethod
    def apply_discount(product_id: str, discount_percent: float) -> bool:
        """
        applies a discount to product in the main products file, updates the product's 'discount_percentage' and 'discounted_price' fields.
        returns true if product found and updated, false otherwise.
        """
        items = ProductsRepo.load_all()
        updated = False
        for it in items:
            if it.get("product_id") == product_id:
                #try to use the number given as actual_price
                try:
                    actual_price = float(it.get("actual_price", "0").replace("$", "").replace(",", ""))
                except Exception:
                    actual_price = 0.0
                #discount must be within 0-100
                disprice = max(0.0, min(float(discount_percent), 100.0))
                discounted_price = actual_price * (1.0 - disprice / 100.0)
                #store values as strings to match existing schema
                it["discount_percentage"] = str(disprice)
                #2 decimal place, if original had $, if not add it back
                formatted = f"{discounted_price:.2f}"
                if isinstance(it.get("actual_price", ""), str) and it.get("actual_price", "").strip().startswith("$"):
                    it["discounted_price"] = f"${formatted}"
                else:
                    it["discounted_price"] = formatted
                updated = True
                break

        if updated:
            ProductsRepo.save_all(items)
            #also record in small discounts index for quick lookup
            discounts = ProductsRepo.load_discounts()
            #remove any existing entry for product_id
            discounts = [d for d in discounts if d.get("product_id") != product_id]
            discounts.append({"product_id": product_id, "discount_percent": float(discount_percent)})
            ProductsRepo.save_discounts(discounts)
        return updated

    #remove discount
    @staticmethod
    def remove_discount(product_id: str) -> bool:
        items = ProductsRepo.load_all()
        updated = False
        for it in items:
            if it.get("product_id") == product_id:
                it.pop("discount_percentage", None)
                it.pop("discounted_price", None)
                updated = True
                break
        if updated:
            ProductsRepo.save_all(items)
            discounts = ProductsRepo.load_discounts()
            discounts = [d for d in discounts if d.get("product_id") != product_id]
            ProductsRepo.save_discounts(discounts)
        return updated

    @staticmethod
    def update_stock(product_id: str, quantity_change: int) -> bool:
        """
        Updates the stock/inventory for a product.
        quantity_change: positive number to add stock, negative to subtract (on purchase).
        Returns True if product found and updated, False otherwise.
        """
        items = ProductsRepo.load_all()
        updated = False

        for it in items:
            if it.get("product_id") == product_id:
                current_stock = int(it.get("quantity", 0)) if it.get("quantity") else 0
                new_stock = max(0, current_stock + quantity_change)
                it["quantity"] = new_stock
                updated = True
                break

        if updated:
            ProductsRepo.save_all(items)

        return updated

