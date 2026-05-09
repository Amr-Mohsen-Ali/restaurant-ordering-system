_order_counter = 1042
_orders = {}


def place_order(cart_items, customer_info):
    if not cart_items:
        return {"success": False, "error": "Cart is empty"}

    if (not customer_info
            or not customer_info.get("name")
            or not customer_info.get("address")):
        return {"success": False, "error": "Missing customer info"}

    global _order_counter
    order_id = f"ORD-{_order_counter}"
    _order_counter += 1

    total = sum(item["price"] * item["quantity"] for item in cart_items)

    _orders[order_id] = {
        "order_id": order_id,
        "items": cart_items,
        "total": total,
        "estimated_time": 25,
        "status": "confirmed",
    }

    return {
        "success": True,
        "order_id": order_id,
        "estimated_time": 25,
    }


def get_confirmation(order_id):
    if not order_id or order_id not in _orders:
        return {"success": False, "error": "Order not found"}
    return _orders[order_id]
