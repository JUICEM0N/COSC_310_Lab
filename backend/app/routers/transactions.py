from fastapi import APIRouter
from backend.app.services.transactions_service import TransactionsService

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/cart/{user_id}", summary="Gets a user's cart summary")
def view_cart_summary(user_id: int):
    """
    This endpoints retrieves the cart summary for a given user. This shows the items
    in the users cart along with the subtotal, and total price (subtotal times TAX_RATE).

    routers/transactions.py -> services/transactions_service.py/TransactionsService.get_cart_summary()
    routers/transactions.py -> repositories/cart_repo.py/CartRepo.cart_exists()
    routers/transactions.py -> repositories/cart_repo.py/CartRepo.get_cart()
    routers/transactions.py -> repositories/products_repo.py/ProductsRepo.get_products()
    
    Args:
        user_id (int): The ID of the user whose cart summary is to be retrieved.
    Returns:
        dict: A dictionary containing the cart summary details including items,
            subtotal, and total price.
    """
    return TransactionsService.get_cart_summary(user_id)

@router.post("/checkout/{user_id}", summary="Creates a transaction for the user")
def checkout(user_id: int):
    """
    This endpoint creates a transaction for the user, effectively checking out their cart,
    which also clears the users cart.

    routers/transactions.py -> services/transactions_service.py/TransactionsService.checkout()
    routers/transactions.py -> repositories/cart_repo.py/CartRepo.cart_exists()
    routers/transactions.py -> repositories/cart_repo.py/CartRepo.get_cart()
    routers/transactions.py -> repositories/transactions_repo.py/TransactionsRepo.create_transaction()
    routers/transactions.py -> repositories/cart_repo.py/CartRepo.clear_cart()
    
    Args:
        user_id (int): The ID of the user who is checking out.
    Returns:
        dict: A dictionary confirming the transaction creation and checkout status.
    """
    return TransactionsService.checkout(user_id)
