from fastapi import APIRouter, status
from typing import List
from backend.app.schemas.item import Item, ItemCreate, ItemUpdate
from backend.app.services.items_service import ItemsService

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("", response_model=List[Item])
def get_items():
    return ItemsService.list_items()

#simple post the payload (is the body of the request)
@router.post("", response_model=Item, status_code=201)
def post_item(payload: ItemCreate):
    return ItemsService.create_item(payload)

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: str):
    return ItemsService.get_item_by_id(item_id)

## We use put here because we are not creating an entirely new item, ie. we keep id the same
@router.put("/{item_id}", response_model=Item)
def put_item(item_id: str, payload: ItemUpdate):
    return ItemsService.update_item(item_id, payload)

## we put the status there becuase in a delete, we wont have a return so it indicates it happened succesfully
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: str):
    ItemsService.delete_item(item_id)
    return None