from langchain.tools import tool
from dotenv import load_dotenv
import requests
import jwt
import os

load_dotenv()

@tool
def place_order(customer_id: int, product_id: int, quantity: int) -> str:
    """Place a new order for a customer.
    IMPORTANT: product_id must be an integer.
    First use get_product_id tool to get the product_id from product name.
    Then use that integer product_id to place the order.
    Input: customer_id (int), product_id (int), quantity (int)
    Output: Return ONLY the confirmation message — no explanation needed."""

    token = os.getenv("USER_TOKEN")
    
    response = requests.post("http://127.0.0.1:8000/orders",
        json={
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "status": "pending"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    data = response.json()
    
    if response.status_code == 200:
        return f"Order placed successfully! Order ID: {data['data']['order_id']}"
    else:
        return "Failed to place order. Please try again."


@tool
def cancel_order(order_id:int) -> str:
    """Cancel a order for a customer.
    Input: order_id
    Output: Cancel Order Successfully"""
    
    token = os.getenv("USER_TOKEN")
    
    response = requests.delete(f"http://127.0.0.1:8000/delete_order/{order_id}",
        headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 200:
        return "Order cancelled successfully!"
    else:
        return "Failed to Cancel order. Please try again."


@tool
def check_order_status(order_id:int) -> str:
    """Check the status of an order.
    Input: order_id
    Output: Returns current order status"""
    
    token = os.getenv("USER_TOKEN")
    
    response = requests.get(f"http://127.0.0.1:8000/orders",
        headers={"Authorization": f"Bearer {token}"})
    
    data = response.json()

    order = next((o for o in data if o["order_id"] == order_id), None)
    if order:
        return f"Order status is: {order['status']}"
    else:
        return "Order not found."


@tool
def modify_order(order_id:int, quantity:int) -> str:
    """Modify/update the quantity of an existing order.
    Input: order_id, quantity
    Output: Update order Successfully"""
    
    token = os.getenv("USER_TOKEN")
    
    response = requests.put(f"http://127.0.0.1:8000/update_order/{order_id}",
        json={
            "customer_id": 1,
            "product_id": 1,
            "quantity": quantity,
            "status": "pending"
        },
        headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 200:
        return "Order updated successfully!"
    else:
        return "Order not found."


@tool
def get_product_id(product_name: str) -> int:
    """Get product id by product name.
    Input: product_name
    Output: product_id"""
    
    response = requests.get("http://127.0.0.1:8000/products?page=1&limit=100")
    data = response.json()
    
    for product in data["data"]:
        if product_name.lower() in product["name"].lower():
            return int(product["id"])
    
    return 0


@tool
def get_my_orders() -> str:
    """Get all orders for the currently logged-in customer.
    Use this when the user wants to see their orders, 
    or when they want to modify/cancel/check status of 
    an order but don't know the order_id.
    No input needed - automatically uses the logged-in user."""

    token = os.getenv("USER_TOKEN")

    payload = jwt.decode(token, options={"verify_signature": False})
    customer_id = payload.get("id")

    orders_response = requests.get(f"http://127.0.0.1:8000/orders",
        headers={"Authorization": f"Bearer {token}"})

    if orders_response.status_code != 200:
        return "Could not fetch your orders."

    orders_data = orders_response.json()
    customer_orders = [o for o in orders_data if o["customer_id"] == customer_id]

    if not customer_orders:
        return "You have no orders yet."

    products_response = requests.get("http://127.0.0.1:8000/products?page=1&limit=100")
    products_data = products_response.json()["data"]
    
    product_names = {p["id"]: p["name"] for p in products_data}

    result = "Here are your orders:\n"
    for i, o in enumerate(customer_orders, 1):
        product_name = product_names.get(o["product_id"], "Unknown product")
        result += f"{i}. {product_name} (Qty: {o['quantity']}) - {o['status']} [Order #{o['order_id']}]\n"
    
    return result