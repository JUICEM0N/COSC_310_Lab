from fastapi import APIRouter, HTTPException, Path, Query, Body
from backend.app.services.wishlist_service import WishlistService
from backend.app.schemas.wishlist import WishlistPrivacyUpdate

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.get("/{user_id}")
def get_wishlist(user_id: int):
    """
    This endpoint retrieves the wishlist for a specific user based on user_id.

    routers/wishlist.py -> services/wishlist_service.py/WishlistService.get_wishlist(user_id)
    
    Args:
        user_id (int): The ID of the user whose wishlist is to be retrieved.
    Returns:
        dict: A dictionary representing the user's wishlist.
    """
    return WishlistService.get_wishlist(user_id)

@router.post("/{user_id}/add")
def add_item(user_id: int, product_id: str, quantity: int = 1):
    """
    This endpoint adds an item to the user's wishlist.

    routers/wishlist.py -> services/wishlist_service.py/WishlistService.add_item(user_id, product_id, quantity)
    
    Args:
        user_id (int): The ID of the user.
        product_id (str): The ID of the product to add.
        quantity (int): The quantity of the product to add. Defaults to 1.
    Returns:
        dict: A message confirming the addition of the item to the wishlist.
    """
    WishlistService.add_item(user_id, product_id, quantity)
    return {"message": f"Added product {product_id} (qty {quantity}) to user {user_id}'s wishlist."}

@router.delete("/{user_id}/remove")
def remove_item(user_id: int, product_id: str):
    """
    This endpoint removes an item from the user's wishlist.

    routers/wishlist.py -> services/wishlist_service.py/WishlistService.remove_item(user_id, product_id)
    
    Args:
        user_id (int): The ID of the user.
        product_id (str): The ID of the product to remove.
    Returns:
        dict: A message confirming the removal of the item from the wishlist.
    """
    WishlistService.remove_item(user_id, product_id)
    return {"message": f"Removed product {product_id} from user {user_id}'s wishlist."}

@router.delete("/{user_id}/clear")
def clear_wishlist(user_id: int):
    """
    This endpoint clears all items from the user's wishlist.

    routers/wishlist.py -> services/wishlist_service.py/WishlistService.clear_wishlist(user_id)
    
    Args:
        user_id (int): The ID of the user.
    Returns:
        dict: A message confirming that the wishlist has been cleared.
    """
    WishlistService.clear_wishlist(user_id)
    return {"message": f"Cleared all items from user {user_id}'s wishlist."}

@router.put("/wishlist/{user_id}/privacy")
def update_wishlist_privacy(user_id: int = Path(...), public: bool = Query(None), body: WishlistPrivacyUpdate = Body(...)):
    """
    This endpoint updates the privacy settings of a user's wishlist.

    routers/wishlist.py -> services/wishlist_service.py/WishlistService.update_privacy(user_id, public, shared_with)
    
    Args:
        user_id (int): The ID of the user.
        public (bool, optional): Whether the wishlist is public. Defaults to None.
        body (WishlistPrivacyUpdate): The request body containing shared_with list.
    Returns:
        dict: A message confirming the update of the wishlist's privacy settings.
    """
    WishlistService.update_privacy(user_id, public, body.shared_with)
    return {"message": "Wishlist privacy updated"}

