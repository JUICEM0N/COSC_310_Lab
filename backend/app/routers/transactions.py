from fastapi import APIRouter, Depends, HTTPException, Request
import stripe
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from backend.app.repositories.transactions_repo import TransactionsRepo
from backend.app.services.transactions_service import TransactionsService
from backend.app.utils.auth import get_current_user
from backend.app.utils.stripe_utils import stripe, verify_webhook
from backend.app.schemas.transaction import PaymentIntentRequest

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/cart/{user_id}", summary="Gets a user's cart summary")
def view_cart_summary(user_id: int, current_user = Depends(get_current_user)):
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
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own cart summary.")
    return TransactionsService.get_cart_summary(user_id)

@router.post("/checkout/{user_id}", summary="Creates a transaction for the user")
def checkout(user_id: int, current_user = Depends(get_current_user)):
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
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only checkout your own cart.")
    return TransactionsService.checkout(user_id)

@router.post("/create-payment-intent/{user_id}", summary="Creates Stripe PaymentIntent")
def create_payment_intent(user_id: int, request: PaymentIntentRequest, current_user=Depends(get_current_user)):
    """
    This endpoint creates a Stripe PaymentIntent for the user to facilitate payment processing.
    routers/transactions.py -> services/transactions_service.py/TransactionsService.create_payment_intent()
    Args:
        user_id (int): The ID of the user for whom the PaymentIntent is to be created.
        request (PaymentIntentRequest): The request body containing currency information.
    Returns:
        dict: A dictionary containing the client secret of the created PaymentIntent.
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(403, "Forbidden")
    try:
        intent = TransactionsService.create_payment_intent(user_id, request.currency)
        return {"client_secret": intent["client_secret"]}
    except stripe.error.StripeError as e:
        raise HTTPException(400, detail=str(e))

@router.post("/confirm-payment/{payment_intent_id}", summary="Manually confirm payment success")
def confirm_payment(payment_intent_id: str, current_user=Depends(get_current_user)):
    """
    Manually confirms a payment if webhooks are not available.
    """
    try:
        return TransactionsService.confirm_payment(payment_intent_id)
    except stripe.error.StripeError as e:
        raise HTTPException(400, detail=str(e))
    
@router.post("/webhook/stripe", summary="Handles Stripe webhooks")
async def stripe_webhook(request: Request):
    """
    This endpoint handles Stripe webhooks for payment events.
    routers/transactions.py -> services/transactions_service.py/TransactionsService.fulfill_transaction()
    Args:
        request (Request): The incoming HTTP request containing the webhook payload.
    Returns:
        dict: A dictionary indicating the success status of the webhook processing.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = verify_webhook(payload, sig_header)
        TransactionsService.fulfill_transaction(event)
        return {"status": "success"}
    except HTTPException as e:
        raise e
    
@router.post("/refund/{transaction_id}", summary="Processes refund")
def process_refund(transaction_id: str, current_user=Depends(get_current_user)):
    """
    This endpoint processes a refund for a given transaction.
    routers/transactions.py -> services/transactions_service.py/TransactionsService.process_refund()
    Args:
        transaction_id (str): The ID of the transaction to be refunded.
    Returns:
        dict: A dictionary containing the refund details.
    """
    transaction = TransactionsRepo.get_transaction_by_id(transaction_id)
    if not transaction or transaction["user_id"] != current_user["user_id"]:
        raise HTTPException(403, "Forbidden")
    return TransactionsService.process_refund(transaction_id)

@router.get("/user/{user_id}", summary="Get user's transaction history")
def get_user_transactions(user_id: int, current_user=Depends(get_current_user)):
    """
    This endpoint retrieves all transactions for a specific user.
    
    Args:
        user_id (int): The ID of the user whose transactions to retrieve.
    Returns:
        list: A list of transactions for the user.
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own transactions.")
    return TransactionsRepo.get_transactions_by_user(user_id)