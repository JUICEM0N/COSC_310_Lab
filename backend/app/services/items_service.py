import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from backend.app.schemas.item import Item, ItemCreate, ItemUpdate
from backend.app.repositories.products_repo import ProductsRepo

class ItemsService:
    def list_items():
        raw = ProductsRepo.load_all()
        items = []

        for it in raw:
            mapped = {
                "id": it.get("id") or it.get("product_id"),
                "product_name": it.get("product_name") or it.get("title"),
                "product_category": it.get("product_category") or it.get("category"),
                "discounted_price": it.get("discounted_price") or "0",
                "actual_price": it.get("actual_price") or "0",
                "discount_percentage": it.get("discount_percentage") or "0%",
                "rating": it.get("rating") or "0",
                "rating_count": it.get("rating_count") or "0",
                "about_product": it.get("about_product") or it.get("description", ""),
                "user_id": it.get("user_id", "0"),
                "user_name": it.get("user_name", "unknown"),
                "review_id": it.get("review_id", "none"),
                "review_title": it.get("review_title", ""),
                "review_content": it.get("review_content", ""),
                "img_link": it.get("img_link", ""),
                "product_link": it.get("product_link", "")
            }
            items.append(Item(**mapped))

        return items

    def create_item(payload: ItemCreate) -> Item:
        items = ProductsRepo.load_all()
        new_id = str(uuid.uuid4())
        if any(it.get("id") == new_id for it in items):  # extremely unlikely, but consistent check
            raise HTTPException(status_code=409, detail="ID collision; retry.")
        # new_item = Item(id=new_id, title=payload.title.strip(), category=payload.category.strip(), tags=payload.tags)
        new_item = Item(
            id=new_id,
            product_name=payload.product_name,
            product_category=payload.product_category,
            discounted_price=payload.discounted_price,
            actual_price=payload.actual_price,
            discount_percentage=payload.discount_percentage,
            rating=payload.rating,
            rating_count=payload.rating_count,
            about_product=payload.about_product,
            user_id=payload.user_id,
            user_name=payload.user_name,
            review_id=payload.review_id,
            review_title=payload.review_title,
            review_content=payload.review_content,
            img_link=payload.img_link,
            product_link=payload.product_link
        )
        items.append(new_item.dict())
        ProductsRepo.save_all(items)
        return new_item

    def get_item_by_id(item_id: str) -> Item:
        items = ProductsRepo.load_all()
        for it in items:
            if it.get("id") == item_id:
                return Item(**it)
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")

    def update_item(item_id: str, payload: ItemUpdate) -> Item:
        items = ProductsRepo.load_all()
        for idx, it in enumerate(items):
            if it.get("id") == item_id:
                updated = Item(
                    id=item_id,
                    title=payload.title.strip(),
                    category=payload.category.strip(),
                    tags=payload.tags,
                )
                items[idx] = updated.dict()
                ProductsRepo.save_all(items)
                return updated
        raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")

    def delete_item(item_id: str) -> None:
        items = ProductsRepo.load_all()
        new_items = [it for it in items if it.get("id") != item_id]
        if len(new_items) == len(items):
            raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")
        ProductsRepo.save_all(new_items)

