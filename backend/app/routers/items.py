from fastapi import APIRouter, status
from typing import List
from backend.app.schemas.item import Item, ItemCreate, ItemUpdate
from backend.app.services.items_service import ItemsService

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("", response_model=List[Item], summary="Lists all items in from our dataset")
def get_items():
    """
    This endpoint returns a list of all the items from our amazon_cad.json file
    
    router/Items.py -> services/items_service.py/ItemsService.list_items() -> ProductsRepo.load_all()
    
    Args:
        None
    Returns:
        List[Item]: A list of all items in the dataset
    """
    return ItemsService.list_items()

#simple post the payload (is the body of the request)
@router.post("", response_model=Item, status_code=201, summary="Creates a new item in our dataset")
def post_item(payload: ItemCreate):
    """
    This endpoint creates a new item in our dataset, and appends it to the amazon_cad.json file
    
    router/Items.py -> services/ItemsService.create_item(payload) -> repositories/ProductsRepo.save_all(items)
    
    Args:
        payload (ItemCreate): The item data to be created
    Returns:
        Item: The created item
    """
    return ItemsService.create_item(payload)

@router.get("/{item_id}", response_model=Item, summary="Retrieves a specific item by its product_id from our dataset")
def get_item(item_id: str):
    """
    This endpoint retrieves a specific item, identified by its product_id

    router/Items.py -> services/items_service.py/ItemsService.get_item_by_id(item_id) -> repositories/products_repo.py/ProductsRepo.product_exists(item_id)
    
    router/Items.py -> services/items_service.py/ItemsService.get_item_by_id(item_id) -> repositories/products_repo.py/ProductsRepo.load_all()
    
    Args:
        item_id (str): The product_id of the item to be retrieved
    Returns:
        Item: The item with the specified product_id
    """
    return ItemsService.get_item_by_id(item_id)

## We use put here because we are not creating an entirely new item, ie. we keep id the same
@router.put("/{item_id}", response_model=Item, summary="Updates existing item in our dataset")
def put_item(item_id: str, payload: ItemUpdate):
    """
    This endpoint updates an exisiting item in our dataset, identified by its product_id, letting the 
    user chose which fields to modify (cannot chnge product_id)

    router/Items.py -> services/items_service.py/ItemsService.update_item(item_id, payload) -> repositories/products_repo.py/ProductsRepo.save_all(items)
    
    router/Items.py -> services/items_service.py/ItemsService.update_item(item_id, payload) -> repositories/products_repo.py/ProductsRepo.product_exists(item_id)
    
    router/Items.py -> services/items_service.py/ItemsService.update_item(item_id, payload) -> repositories/products_repo.py/ProductsRepo.load_all()
    
    Args:
        item_id (str): The product_id of the item to be updated
        payload (ItemUpdate): The item data to be updated
    Returns:
        Item: The updated item
    """
    return ItemsService.update_item(item_id, payload)

## we put the status there becuase in a delete, we wont have a return so it indicates it happened succesfully
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletes item from our dataset")
def remove_item(item_id: str):
    """
    This endpoint deeletes an item from our dataset, identified but its product_id

    router/Items.py -> services/items_service.py/ItemsService.delete_item(item_id) -> repositories/products_repo.py/ProductsRepo.product_exists(item_id)
    
    router/Items.py -> services/items_service.py/ItemsService.delete_item(item_id) -> repositories/products_repo.py/ProductsRepo.load_all()
    
    router/Items.py -> services/items_service.py/ItemsService.delete_item(item_id) -> repositories/products_repo.py/ProductsRepo.save_all(items)
    
    Args:
        item_id (str): The product_id of the item to be deleted
    Returns:
        None
    """
    ItemsService.delete_item(item_id)
    return None