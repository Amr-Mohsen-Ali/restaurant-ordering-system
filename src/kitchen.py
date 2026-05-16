"""Kitchen display blueprint.

Provides:
  GET /kitchen         — standalone kitchen display page (staff/admin only)
  GET /api/kitchen/orders — JSON order data grouped by display column
"""
from flask import Blueprint, jsonify, render_template

from src import auth
from src.constants import (
    ORDER_STATUS_DELIVERED,
    ORDER_STATUS_OUT_FOR_DELIVERY,
    ORDER_STATUS_PREPARING,
    ROLE_ADMIN,
    ROLE_STAFF,
)
from src.database import Order

kitchen_bp = Blueprint("kitchen", __name__)

# Map Flask statuses → kitchen display columns
# Preparing       → "received"  (New Orders column)
# Out for Delivery → "preparing" (Preparing column)
# Delivered       → "served"    (Recently Served column)
_STATUS_TO_COLUMN = {
    ORDER_STATUS_PREPARING: "received",
    ORDER_STATUS_OUT_FOR_DELIVERY: "preparing",
    ORDER_STATUS_DELIVERED: "served",
}


@kitchen_bp.route("/kitchen")
@auth.login_required
@auth.require_role(ROLE_STAFF, ROLE_ADMIN)
def kitchen_display():
    """Render the standalone kitchen display page."""
    return render_template("kitchen.html")


@kitchen_bp.route("/api/kitchen/orders")
@auth.login_required
@auth.require_role(ROLE_STAFF, ROLE_ADMIN)
def kitchen_orders_api():
    """Return orders grouped into kitchen display columns."""
    orders = Order.query.order_by(Order.created_at.asc()).all()

    columns = {"received": [], "preparing": [], "ready": [], "served": []}
    served_limit = 10  # Only show last 10 served orders

    for order in orders:
        col = _STATUS_TO_COLUMN.get(order.status)
        if col is None:
            continue

        entry = {
            "id": order.id,
            "status": order.status,
            "column": col,
            "customer_name": order.customer_name or "Guest",
            "customer_address": order.customer_address or "",
            "items": order.order_items or [],
            "total": order.total,
            "estimated_time": order.estimated_time,
            "created_at": order.created_at.isoformat() if order.created_at else None,
        }
        columns[col].append(entry)

    # Limit served to last N, most recent last
    columns["served"] = columns["served"][-served_limit:]

    return jsonify({
        "success": True,
        "columns": columns,
        "counts": {k: len(v) for k, v in columns.items()},
    })
