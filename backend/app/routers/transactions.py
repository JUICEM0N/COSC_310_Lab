from fastapi import APIRouter
from backend.app.services.transactions_service import TransactionsService

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/cart/{user_id}")
def view_cart_summary(user_id: int):
    return TransactionsService.get_cart_summary(user_id)

@router.post("/checkout/{user_id}")
def checkout(user_id: int):
    return TransactionsService.checkout(user_id)
