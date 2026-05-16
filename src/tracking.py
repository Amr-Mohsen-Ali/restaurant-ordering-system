"""Order tracking feature.

This file contains the order tracking business logic and Flask blueprint routes.
"""

from flask import Blueprint, jsonify, request, render_template
from src.database import db, Order

tracking_bp = Blueprint("tracking", __name__)
VALID_STATUSES = ["Preparing", "Out for Delivery", "Delivered"]


def is_empty_order_id(order_id):
    """Return True when the customer did not enter a usable order ID."""
    return order_id is None or order_id.strip() == ""


def get_order_status(order_id):
    """Return the status for a valid order ID."""
    order = Order.query.get(order_id.strip())
    if not order:
        raise ValueError("Invalid order ID")
    return order.status


def get_order_details(order_id):
    """Return the full order details for a valid order ID."""
    order = Order.query.get(order_id.strip())
    if not order:
        raise ValueError("Invalid order ID")
    return order.to_dict()


def update_order_status(order_id, new_status):
    """Update an order status when the status is allowed."""
    order = Order.query.get(order_id.strip())
    if not order:
        raise ValueError("Invalid order ID")
    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid status")
    order.status = new_status
    db.session.commit()
    return order.to_dict()


def advance_order_status(order_id):
    """Move an order to the next tracking status for demo simulation."""
    current_status = get_order_status(order_id)
    current_index = VALID_STATUSES.index(current_status)
    next_index = min(current_index + 1, len(VALID_STATUSES) - 1)
    return update_order_status(order_id, VALID_STATUSES[next_index])


@tracking_bp.route("/")
@tracking_bp.route("/tracking")
def tracking_page():
    """Show the customer order tracking page."""
    return render_template("tracking.html")


@tracking_bp.route("/track/<path:order_id>")
def track_order(order_id):
    """Return the status for one order ID using the team API format."""
    if is_empty_order_id(order_id):
        return jsonify({"success": False, "error": "Order ID is required"}), 400

    try:
        order = get_order_details(order_id)
    except ValueError:
        return jsonify({"success": False, "error": "Invalid order ID"}), 404

    return jsonify({"success": True, "status": order["status"], "order": order}), 200


@tracking_bp.route("/track/<path:order_id>/status", methods=["POST"])
def change_order_status(order_id):
    """Update an order status for project demo purposes."""
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")

    try:
        order = update_order_status(order_id, new_status)
    except ValueError as error:
        status_code = 404 if str(error) == "Invalid order ID" else 400
        return jsonify({"success": False, "error": str(error)}), status_code

    return jsonify({"success": True, "status": order["status"], "order": order}), 200


@tracking_bp.route("/track/<path:order_id>/advance", methods=["POST"])
def advance_order(order_id):
    """Advance an order to the next status for project demo purposes."""
    try:
        order = advance_order_status(order_id)
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 404

    return jsonify({"success": True, "status": order["status"], "order": order}), 200