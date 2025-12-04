import crypt
import requests
from datetime import datetime
from backend.app.repositories.users_repo import UsersRepo
from backend.app.repositories.cart_repo import CartRepo
from backend.app.repositories.products_repo import ProductsRepo

class ReceiptService:

    TAX_RATE = 0.12

    def validate_user_email(user_id: int) -> str:
        user = UsersRepo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User does not exist")

        email = user.get("email")
        if not email or "@" not in email:
            raise ValueError("User email invalid or missing")

        return email

    def image_exists(url: str) -> bool:
        try:
            r = requests.head(url, timeout=2)
            return r.status_code == 200
        except:
            return False

    def build_order(user_id: int) -> dict:
        cart = CartRepo.get_cart(user_id)
        if not cart or len(cart.get("items", [])) == 0:
            raise ValueError("Cart is empty")

        products = ProductsRepo.load_products()

        product_lookup = {}
        for p in products:
            product_id = str(p.get("product_id", "")).strip()
            if product_id:
                product_lookup[product_id] = p

        items = []
        subtotal = 0

        for item in cart["items"]:
            product_id = str(item["product_id"]).strip()

            if product_id not in product_lookup:
                raise ValueError(f"Product '{product_id}' does not exist")

            product = product_lookup[product_id]

            quantity = item["quantity"]

            discounted_price_str = product.get("discounted_price", "$0").replace("$", "").replace(",", "")
            price_per_unit = float(discounted_price_str)

            line_total = round(price_per_unit * quantity, 2)
            subtotal += line_total

            image_url = product.get("img_link", "")
            image_valid = ReceiptService.image_exists(image_url)

            items.append({
                "product_id": product_id,
                "name": product.get("product_name", "Unknown product"),
                "quantity": quantity,
                "price_per_unit": price_per_unit,
                "subtotal": line_total,
                "actual_price": product.get("actual_price", ""),
                "discount": product.get("discount_percentage", ""),
                "category": product.get("category", ""),
                "rating": product.get("rating", ""),
                "rating_count": product.get("rating_count", ""),
                "image": image_url if image_valid else None,
            })

        tax = round(subtotal * ReceiptService.TAX_RATE, 2)
        total = round(subtotal + tax, 2)

        return {
            "user_id": user_id,
            "items": items,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "timestamp": datetime.now().isoformat()
        }

    def generate_receipt_hash(order: dict) -> str:
        raw = f"{order['user_id']}{order['total']}{order['timestamp']}"
        salt = crypt.mksalt(crypt.METHOD_SHA512)
        hashed = crypt.crypt(raw, salt)

        cleaned = hashed.replace("/", "").replace(".", "").replace("$", "")
        return cleaned[:32]

    def generate_html_receipt(order: dict, receipt_id: str) -> str:
        rows = ""

        for item in order["items"]:
            img_html = (
                f'<img src="{item["image"]}" width="100" />'
                if item["image"]
                else '<div style="width:100px;height:100px;background:#eee;display:flex;align-items:center;justify-content:center;color:#666;">No Image</div>'
            )

            rows += f"""
            <tr style="border-bottom: 1px solid #ccc;">
                <td>{img_html}</td>

                <td style="padding-left:10px;">
                    <b>{item['name']}</b><br>
                    <small>Product ID: {item['product_id']}</small><br>
                    <small>Category: {item['category']}</small><br>
                    <small>Rating: {item['rating']} ⭐ ({item['rating_count']} reviews)</small><br>
                    <small>Discount: {item['discount']}</small><br>
                    <small>Original Price: {item['actual_price']}</small>
                </td>

                <td style="text-align:center;">{item['quantity']}</td>
                <td style="text-align:center;">${item['price_per_unit']}</td>
                <td style="text-align:center;">${item['subtotal']}</td>
            </tr>
            """

        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">

            <h1 style="color:#444;">Your StackSquad Receipt</h1>

            <p><b>Receipt ID:</b> {receipt_id}</p>
            <p><b>Date:</b> {order['timestamp']}</p>

            <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse: collapse;">
                <tr style="background:#f8f8f8;border-bottom:2px solid #ccc;">
                    <th>Image</th>
                    <th>Product</th>
                    <th>Qty</th>
                    <th>Price/Unit</th>
                    <th>Subtotal</th>
                </tr>
                {rows}
            </table>

            <h3 style="margin-top:20px;">Subtotal: ${order['subtotal']}</h3>
            <h3>Tax: ${order['tax']}</h3>
            <h2>Total: ${order['total']}</h2>

            <p style="margin-top:20px;font-size:12px;color:#777;">
                Receipt Hash: <code>{receipt_id}</code>
            </p>

        </body>
        </html>
        """