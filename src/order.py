import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

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


# --- Item resolution (stub — wire to src/menu.py later) ---

_SAMPLE_ITEMS = {
    "1": {"id": "1", "name": "Burger", "price": 9.99, "quantity": 1},
    "2": {"id": "2", "name": "Fries", "price": 3.99, "quantity": 1},
}


def _resolve_items(item_ids):
    return [_SAMPLE_ITEMS[i] for i in item_ids if i in _SAMPLE_ITEMS]


def _demo_cart():
    return [_SAMPLE_ITEMS["1"], _SAMPLE_ITEMS["2"]]


def _cart_total(cart):
    return sum(item["price"] * item["quantity"] for item in cart)


# --- JSON API routes ---

@order_bp.route('/place-order', methods=['POST'])
def place_order_view():
    data = request.get_json(silent=True) or {}
    cart = _resolve_items(data.get('items', []))
    customer = data.get('customer')
    result = place_order(cart, customer)
    if result["success"]:
        return jsonify(result), 201
    return jsonify(result), 400


@order_bp.route('/confirmation/<order_id>', methods=['GET'])
def confirmation_view(order_id):
    result = get_confirmation(order_id)
    if "status" in result:
        return jsonify(result), 200
    return jsonify(result), 404


@order_bp.route('/cancel-order/<order_id>', methods=['POST'])
def cancel_order_view(order_id):
    result = cancel_order(order_id)
    if result["success"]:
        return jsonify(result), 200
    if result.get("error") == "Order not found":
        return jsonify(result), 404
    return jsonify(result), 400


# --- HTML UI routes ---

@order_bp.route('/checkout', methods=['GET'])
def checkout_view():
    cart = [] if request.args.get('empty') == '1' else _demo_cart()
    return render_template(
        "checkout.html",
        view="cart",
        cart=cart,
        cart_total=_cart_total(cart),
    )


@order_bp.route('/checkout', methods=['POST'])
def checkout_submit():
    cart = _demo_cart()
    customer = {
        "name": request.form.get("name", "").strip(),
        "address": request.form.get("address", "").strip(),
    }
    result = place_order(cart, customer)
    if result["success"]:
        return redirect(url_for("order.checkout_confirmation", order_id=result["order_id"]))
    return render_template(
        "checkout.html",
        view="cart",
        cart=cart,
        cart_total=_cart_total(cart),
        error=result["error"],
        form_name=customer["name"],
        form_address=customer["address"],
    )


@order_bp.route('/checkout/confirmation/<order_id>', methods=['GET'])
def checkout_confirmation(order_id):
    result = get_confirmation(order_id)
    if "status" in result:
        return render_template("checkout.html", view="confirmation", order=result)
    return render_template(
        "checkout.html",
        view="error",
        error=result.get("error", "Order not found"),
    ), 404


@order_bp.route('/checkout/cancel/<order_id>', methods=['POST'])
def checkout_cancel(order_id):
    result = cancel_order(order_id)
    if result["success"]:
        return render_template("checkout.html", view="cancelled", order_id=order_id)
    confirmation_data = get_confirmation(order_id)
    if "status" in confirmation_data:
        return render_template(
            "checkout.html",
            view="confirmation",
            order=confirmation_data,
            cancel_error=result["error"],
        )
    return render_template(
        "checkout.html",
        view="error",
        error=result.get("error", "Order not found"),
    ), 404
