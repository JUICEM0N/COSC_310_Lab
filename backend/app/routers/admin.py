from fastapi import APIRouter, Depends, HTTPException, Body
from backend.app.schemas.penalty import PenaltyCreate
from backend.app.schemas.admin import PromoteUser
from backend.app.services.admin_service import AdminService
from backend.app.services.users_service import UsersService
from backend.app.repositories.products_repo import ProductsRepo

router = APIRouter(prefix="/admin", tags=["Admin"])
service = AdminService()

def require_admin(user = Depends(UsersService.get_user_info)):
    if not user or not isinstance(user, dict):
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not user.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.post("/promote", summary="Promote a user to admin")
def promote(data: PromoteUser, admin = Depends(require_admin)):
    """
    This endpoint promotes a user to admin status.

    routers/admin.py -> services/admin_service.py/AdminService.promote_user(data.user_id) 

    Args:
        data (PromoteUser): The user promotion data.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success.
    """
    ok = service.promote_user(data.user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": f"User {data.user_id} promoted to admin"}

@router.post("/penalty", summary="Apply a penalty to a user")
def penalty(data: PenaltyCreate, admin = Depends(require_admin)):
    """
    This endpoint applies a penalty to a user.

    routers/admin.py -> services/admin_service.py/AdminService.apply_penalty(data)

    Args:
        data (PenaltyCreate): The penalty data.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success and the penalty ID.
    """
    pid = service.apply_penalty(
        data.user_id,
        data.reason,
        data.amount,
        data.status
    )
    return {
        "msg": "Penalty applied",
        "penalty_id": pid
    }

@router.get("/penalties/{user_id}", summary="Get penalties for a user")
def get_penalties(user_id: int, admin = Depends(require_admin)):
    """
    This endpoint retrieves all penalties for a specific user.
    
    routers/admin.py -> services/admin_service.py/AdminService.get_user_penalties(user_id)
    
    Args:
        user_id (int): The ID of the user whose penalties are to be retrieved.
        admin: The current admin user (injected by dependency).
    Returns:
        list: A list of penalties for the user.
    """
    return service.get_user_penalties(user_id)

@router.post("/discount/{product_id}", summary="Apply a discount to a product")
def apply_discount(product_id: str, percent: float | int, admin = Depends(require_admin)):
    """
    This endpoint applies a discount to a specific product.
    
    routers/admin.py -> repositories/products_repo.py/ProductsRepo.apply_discount(product_id, percent)
    
    Args:
        product_id (str): The ID of the product to which the discount is to be applied.
        percent (float): The discount percentage to apply.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success and the discount percentage applied.
    """
    ok = ProductsRepo.apply_discount(product_id, percent)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")

    return {
        "msg": f"Discount applied to {product_id}",
        "discount_percent": percent
    }
@router.delete("/discount/{product_id}", summary="Remove a discount from a product")
def remove_discount(product_id: str, admin = Depends(require_admin)):
    """
    This endpoint removes a discount from a product.
    
    routers/admin.py -> repositories/products_repo.py/ProductsRepo.remove_discount(product_id)
    
    Args:
        product_id (str): The ID of the product from which the discount is to be removed.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success.
    """
    ok = ProductsRepo.remove_discount(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")

    return {"msg": f"Discount removed from {product_id}"}

@router.post("/products-of-week", summary="Set the products of the week")
def set_products_of_week(product_ids: list[str] = Body(..., embed=True), admin = Depends(require_admin)):
    """
    This endpoint sets the product or products of the week.
    
    routers/admin.py -> repositories/products_repo.py/ProductsRepo.set_products_of_the_week(product_ids)
    
    Args:
        product_ids (list[str]): A list of product IDs to set as products of the week.
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A message indicating success and the list of product IDs set.
    """
    ProductsRepo.set_products_of_the_week(product_ids)
    return {
        "msg": "Products of the week updated",
        "products": product_ids
    }


@router.get("/products-of-week", summary="Get the current products of the week")
def get_products_of_week(admin = Depends(require_admin)):
    """
    This endpoint retrieves all products of the week.
    
    routers/admin.py -> repositories/products_repo.py/ProductsRepo.get_products_of_the_week()
    
    Args:
        admin: The current admin user (injected by dependency).
    Returns:
        dict: A dictionary containing the list of products of the week.
    """
    items = ProductsRepo.get_products_of_the_week()
    return {"products_of_week": items}
