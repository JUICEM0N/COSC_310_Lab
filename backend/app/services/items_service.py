import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from backend.app.schemas.item import Item, ItemCreate, ItemUpdate
from backend.app.repositories.products_repo import ProductsRepo

class ItemsService:

    def list_items():
        return ProductsRepo.load_all()

    def create_item(payload: ItemCreate) -> Item:
        items = ProductsRepo.load_all()
        new_id = str(uuid.uuid4())
        if any(it.get("product_id") == new_id for it in items):  # extremely unlikely, but consistent check
            raise HTTPException(status_code=409, detail="ID collision; retry.")
        # new_item = Item(
        #     product_id=new_id,
        #     product_name=payload.product_name,
        #     category=payload.product_category,
        #     discounted_price=payload.discounted_price,
        #     actual_price=payload.actual_price,
        #     discount_percentage=payload.discount_percentage,
        #     rating=payload.rating,
        #     rating_count=payload.rating_count,
        #     about_product=payload.about_product,
        #     user_id=payload.user_id,
        #     user_name=payload.user_name,
        #     review_id=payload.review_id,
        #     review_title=payload.review_title,
        #     review_content=payload.review_content,
        #     img_link=payload.img_link,
        #     product_link=payload.product_link
        # )

        new_item = Item(
            product_id=new_id,
            product_name=payload.product_name,
            category=payload.category,
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

        items.append(new_item.model_dump())
        ProductsRepo.save_all(items)
        return new_item

    def get_item_by_id(item_id: str) -> Item:
        if not ProductsRepo.product_exists(item_id):
            raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")

        items = ProductsRepo.load_all()
        for it in items:
            if it.get("product_id") == item_id:
                return Item(
                    product_id=it.get("product_id"),
                    product_name=it.get("product_name"),
                    category=it.get("category"),
                    discounted_price=it.get("discounted_price"),
                    actual_price=it.get("actual_price"),
                    discount_percentage=it.get("discount_percentage"),
                    rating=it.get("rating"),
                    rating_count=it.get("rating_count"),
                    about_product=it.get("about_product"),
                    user_id=it.get("user_id"),
                    user_name=it.get("user_name"),
                    review_id=it.get("review_id"),
                    review_title=it.get("review_title"),
                    review_content=it.get("review_content"),
                    img_link=it.get("img_link"),
                    product_link=it.get("product_link")
                )

                # return Item(**mapped)

    def update_item(item_id: str, payload: ItemUpdate) -> Item:
        if not ProductsRepo.product_exists(item_id):
            raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")

        items = ProductsRepo.load_all()
        for idx, it in enumerate(items):
            if it.get("product_id") == item_id:
                updated = Item(
                    product_id=item_id,
                    product_name=payload.product_name,
                    category=payload.category,
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

                items[idx] = updated.model_dump()
                ProductsRepo.save_all(items)

                return updated
            
        # raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")

    def delete_item(item_id: str) -> None:
        if not ProductsRepo.product_exists(item_id):
            raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")

        items = ProductsRepo.load_all()
        new_items = [it for it in items if it.get("product_id") != item_id]
        
        if len(new_items) == len(items):
            raise HTTPException(status_code=404, detail=f"Item '{item_id}' not found")
        
        ProductsRepo.save_all(new_items)