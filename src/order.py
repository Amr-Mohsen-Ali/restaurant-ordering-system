import datetime

from flask import Blueprint, jsonify

order_bp = Blueprint('order', __name__)

CANCEL_WINDOW = datetime.timedelta(minutes=2)

_order_counter = 1042
_orders = {}
_placed_at = {}


def _now():
    return datetime.datetime.now()


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
    _placed_at[order_id] = _now()

    return {
        "success": True,
        "order_id": order_id,
        "status": "confirmed",
        "estimated_time": 25,
    }


def get_confirmation(order_id):
    if not order_id or order_id not in _orders:
        return {"success": False, "error": "Order not found"}
    return _orders[order_id]


def cancel_order(order_id):
    if not order_id or order_id not in _orders:
        return {"success": False, "error": "Order not found"}

    age = _now() - _placed_at[order_id]
    if age > CANCEL_WINDOW:
        return {"success": False, "error": "Cannot cancel confirmed order"}

    return {"success": True, "message": "Order cancelled"}


# --- Routes (stub preserved; replaced in a later commit) ---

@order_bp.route('/place-order', methods=['POST'])
def place_order_view():
    return jsonify({'order_id': '123', 'status': 'Preparing'}), 201
