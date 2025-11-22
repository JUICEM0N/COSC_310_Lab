from fastapi import APIRouter, HTTPException
from backend.app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/{user_id}", summary="Get user's cart")
def get_cart(user_id: int):
    """
    This endpoint retrieves the cart for a specific user based on user_id.

    routers/cart.py -> services/cart_service.py/CartService.get_cart(user_id) -> 
    repositories/cart_repo.py/CartRepo.get_cart(user_id) 

    routers/cart.py -> services/cart_service.py/CartService.get_cart(user_id) -> 
    repositories/cart_repo.py/CartRepo.cart_exists(user_id)

    routers/cart.py -> services/cart_service.py/CartService.get_cart(user_id) -> 
    repositories/users_repo.py/UsersRepo.user_exists(user_id)

    Args:
        user_id (int): The ID of the user whose cart is to be retrieved.
    Returns:
        dict: A dictionary representing the user's cart.
    """
    return CartService.get_cart(user_id)

@router.post("/{user_id}/add", summary="Add item to cart")
def add_item(user_id:int, product_id: str, quantity: int = 1):
    """
    This endpoint adds an item to the user's cart.

    routers/cart.py -> services/cart_service.py/CartService.add_item(user_id, product_id, quantity) -> 
    repositories/cart_repo.py/CartRepo.add_item(user_id, product_id, quantity)
    
    Args:
        user_id (int): The ID of the user.
        product_id (str): The ID of the product to add.
        quantity (int): The quantity of the product to add. Defaults to 1.
    Returns:
        dict: A message confirming the addition of the item to the cart.
    """
    CartService.add_item(user_id, product_id, quantity)
    return {"message": f"{product_id} added to cart {user_id}"}

@router.patch("/{user_id}/update", summary="Update item quantity in cart")
def update_quantity(user_id: int, product_id: str, quantity: int):
    """
    This endpoint updates the quantity of a specific item in the user's cart.
    
    routers/cart.py -> services/cart_service.py/CartService.update_quantity(user_id, product_id, quantity) -> 
    repositories/cart_repo.py/CartRepo.update_quantity(user_id, product_id, quantity)
    
    Args:
        user_id (int): The ID of the user.
        product_id (str): The ID of the product to update.
        quantity (int): The new quantity for the product.
    Returns:
        dict: A message confirming the update of the item's quantity in the cart.
    """
    CartService.update_quantity(user_id, product_id, quantity)
    return {"message": "Quantity updated"}

@router.delete("/{user_id}/remove", summary="Remove item from cart")
def remove_item(user_id: int, product_id: str):
    """
    This endpoint removes a specific item from the user's cart.

    routers/cart.py -> services/cart_service.py/CartService.remove_item(user_id, product_id) -> 
    repositories/cart_repo.py/CartRepo.remove_item(user_id, product_id)

    Args:
        user_id (int): The ID of the user.
        product_id (str): The ID of the product to remove.
    Returns:
        dict: A message confirming the removal of the item from the cart.
    """
    CartService.remove_item(user_id, product_id)
    return {"message": f"{product_id} removed from cart {user_id}"}

@router.delete("/{user_id}/clear", summary="Clear user's cart")
def clear_cart(user_id: int):
    """
    This endpoint clears all items from the user's cart.
    
    routers/cart.py -> services/cart_service.py/CartService.clear_cart(user_id) -> 
    repositories/cart_repo.py/CartRepo.clear_cart(user_id)

    Args:
        user_id (int): The ID of the user.
    Returns:
        dict: A message confirming that the cart has been cleared.
    """
    CartService.clear_cart(user_id)
    return {"message": f"Cleared cart for {user_id}"}