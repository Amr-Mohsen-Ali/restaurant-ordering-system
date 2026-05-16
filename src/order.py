import datetime
import os

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from src.database import db, Order
from src.cart import current_cart

order_bp = Blueprint('order', __name__)

CANCEL_WINDOW = datetime.timedelta(minutes=2)

ORDER_COUNTER_FILE = os.path.join(os.path.dirname(__file__), '..', 'instance', 'order_counter.txt')


def get_next_order_id():
    try:
        with open(ORDER_COUNTER_FILE, 'r') as f:
            counter = int(f.read())
    except:
        counter = 1000
    counter += 1
    with open(ORDER_COUNTER_FILE, 'w') as f:
        f.write(str(counter))
    return str(counter)


def place_order(cart_items, customer_info):
    if not cart_items:
        return {"success": False, "error": "Cart is empty"}

    if (not customer_info
            or not customer_info.get("name")
            or not customer_info.get("address")):
        return {"success": False, "error": "Missing customer info"}

    order_id = get_next_order_id()
    total = sum(item["price"] * item["quantity"] for item in cart_items)

    order = Order(
        id=order_id,
        items=cart_items,
        total=round(total, 2),
        status='Preparing',
        customer_name=customer_info['name'],
        customer_address=customer_info['address'],
        estimated_time=25
    )
    db.session.add(order)
    db.session.commit()

    return {
        "success": True,
        "order_id": order_id,
        "status": "Preparing",
        "estimated_time": 25,
    }


def get_confirmation(order_id):
    order = Order.query.get(order_id)
    if not order:
        return {"success": False, "error": "Order not found"}
    return order.to_dict()


def cancel_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return {"success": False, "error": "Order not found"}

    if order.status in ['Ready', 'Delivered']:
        return {"success": False, "error": f"Cannot cancel {order.status.lower()} order"}

    age = datetime.datetime.utcnow() - order.created_at
    if age > CANCEL_WINDOW:
        return {"success": False, "error": "Cannot cancel order after 2 minutes"}

    order.status = 'Cancelled'
    db.session.commit()
    return {"success": True, "message": "Order cancelled", "order_id": order_id}


# --- JSON API routes ---

@order_bp.route('/place-order', methods=['POST'])
def place_order_view():
    data = request.get_json(silent=True) or {}
    cart = data.get('items', [])
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
    cart = [] if request.args.get('empty') == '1' else current_cart["items"]
    return render_template(
        "checkout.html",
        view="cart",
        cart=cart,
        cart_total=current_cart["total"],
    )


@order_bp.route('/checkout', methods=['POST'])
def checkout_submit():
    cart = current_cart["items"]
    customer = {
        "name": request.form.get("name", "").strip(),
        "address": request.form.get("address", "").strip(),
    }
    result = place_order(cart, customer)
    if result["success"]:
        current_cart["items"] = []
        current_cart["total"] = 0.00
        return redirect(url_for("order.checkout_confirmation", order_id=result["order_id"]))
    return render_template(
        "checkout.html",
        view="cart",
        cart=cart,
        cart_total=current_cart["total"],
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
