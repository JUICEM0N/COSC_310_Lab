from repositories.cart_repo import CartRepo
from repositories.products_repo import ProductsRepo

class CartService:
    
    def get_cart(user_id: int):
        return CartRepo.get_cart(user_id)
    
    def add_item(user_id: int, product_id: str, quantity: int = 1):
        product = ProductsRepo.get_product(product_id)

        if not product:
            raise ValueError(f"Product does not exist: {product_id}")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        CartRepo.add_item(user_id, product_id, quantity)

    def update_quantity(user_id: int, product_id: str, quantity: int):
        product = ProductsRepo.get_products(product_id)
        
        if not product:
            raise ValueError(f"Product does not exist: {product_id}")
        
        CartRepo.update_quantity(user_id, product_id, quantity)

    def remove_item(user_id: int, product_id: str):
        CartRepo.remove_item(user_id, product_id)

    def clear_cart(user_id: int):
        CartRepo.cleart_cart(user_id)