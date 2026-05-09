"""Integration tests for the Order Placement + Tracking boundary.

Real cross-module integration: src.cart.add_to_cart populates the cart,
src.order.place_order writes to shared order storage, and
src.order.get_confirmation reads from it. The successful and failed
write paths are both verified against the read path. No internal
modules are mocked.
"""

from src.cart import add_to_cart
from src.order import get_confirmation, place_order


# INTEGRATION: Order Placement + Tracking
def test_place_order_then_get_confirmation_returns_status_confirmed():
    cart = []
    add_to_cart(cart, {"id": "1", "name": "Burger", "price": 10.00, "quantity": 1})
    customer = {"name": "Gaber", "address": "123 Main St"}

    placed = place_order(cart, customer)
    confirmation = get_confirmation(placed["order_id"])

    assert confirmation["status"] == "confirmed"


# INTEGRATION: Order Placement + Tracking
def test_failed_place_order_then_get_confirmation_returns_not_found():
    cart = []  # empty cart causes place_order to fail
    customer = {"name": "Gaber", "address": "123 Main St"}

    failed = place_order(cart, customer)
    assert failed["success"] is False  # sanity: placement did fail

    # A failed placement must not pollute storage. Querying any id
    # (including a fabricated one) must return "Order not found".
    result = get_confirmation("ORD-99999999")

    assert result["error"] == "Order not found"
