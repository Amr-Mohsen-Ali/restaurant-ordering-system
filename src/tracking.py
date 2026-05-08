"""Order tracking feature.

This file contains the order tracking business logic and Flask blueprint routes.
"""

from flask import Blueprint, jsonify, render_template

from src.data.orders import ORDERS


tracking_bp = Blueprint("tracking", __name__)


def is_empty_order_id(order_id):
    """Return True when the customer did not enter a usable order ID."""
    return order_id is None or order_id.strip() == ""


def get_order_status(order_id):
    """Return the status for a valid order ID.

    Raises:
        ValueError: If the order ID does not exist.
    """
    cleaned_order_id = order_id.strip()

    if cleaned_order_id not in ORDERS:
        raise ValueError("Invalid order ID")

    return ORDERS[cleaned_order_id]["status"]


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
        status = get_order_status(order_id)
    except ValueError:
        return jsonify({"success": False, "error": "Invalid order ID"}), 404

    return jsonify({"success": True, "status": status}), 200