from backend.app.repositories.cart_repo import CartRepo
from backend.app.repositories.products_repo import ProductsRepo
from backend.app.repositories.users_repo import UsersRepo
from fastapi import HTTPException

class CartService:
    
    def get_cart(user_id: int):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"User does not exist: {user_id}")

        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart does not exist for user: {user_id}")
        
        return CartRepo.get_cart(user_id)
    
    def add_item(user_id: int, product_id: str, quantity: int = 1):
        CartService.validate_items(user_id, product_id, quantity)
        
        product = ProductsRepo.get_products(product_id)
        available_stock = int(product.get("quantity", 0))
        
        cart = CartRepo.get_cart(user_id)
        current_qty = 0
        if cart:
            existing_item = next((i for i in cart["items"] if i["product_id"] == product_id), None)
            if existing_item:
                current_qty = existing_item["quantity"]
        
        if current_qty + quantity > available_stock:
            raise HTTPException(status_code=400, detail=f"Insufficient stock. Only {available_stock} available.")

        CartRepo.add_item(user_id, product_id, quantity)

    def update_quantity(user_id: int, product_id: str, quantity: int):
        CartService.validate_items(user_id, product_id, quantity)

        if not CartRepo.item_in_cart(user_id, product_id):
            raise HTTPException(status_code=404, detail=f"Item not found in cart: {product_id}")
        
        product = ProductsRepo.get_products(product_id)
        available_stock = int(product.get("quantity", 0))
        
        if quantity > available_stock:
            raise HTTPException(status_code=400, detail=f"Insufficient stock. Only {available_stock} available.")
        
        CartRepo.update_quantity(user_id, product_id, quantity)

    def remove_item(user_id: int, product_id: str):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"User does not exist: {user_id}")

        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart does not exist for user: {user_id}")
        
        if not CartRepo.item_in_cart(user_id, product_id):
            raise HTTPException(status_code=404, detail=f"Item not found in cart: {product_id}")
        
        CartRepo.remove_item(user_id, product_id)

    def clear_cart(user_id: int):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"User does not exist: {user_id}")

        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart does not exist for user: {user_id}")
        
        CartRepo.clear_cart(user_id)

    def validate_items(user_id: int, product_id: str, quantity: int):
        if not UsersRepo.user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"User does not exist: {user_id}")
        
        if not ProductsRepo.product_exists(product_id):
            raise HTTPException(status_code=404, detail=f"Product does not exist: {product_id}")
        
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
        
        if not CartRepo.cart_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Cart does not exist for user: {user_id}")