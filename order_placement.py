_order_counter = 1042


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

    return {
        "success": True,
        "order_id": order_id,
        "estimated_time": 25,
    }
