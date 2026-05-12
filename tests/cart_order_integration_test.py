"""Integration tests for the Cart + Order Placement boundary.

Real cross-module integration: src.cart.add_to_cart constructs the cart,
then src.order.place_order processes it, and src.order.get_confirmation
reads the resulting order. No internal modules are mocked — the full
write-then-read path runs for real.
"""

from src.cart import add_to_cart
from src.order import get_confirmation, place_order


# INTEGRATION: Cart + Order Placement
def test_addtocart_then_place_order_total_matches_cart_total():
    cart = []
    add_to_cart(cart, {"id": "1", "name": "Burger", "price": 10.00, "quantity": 1})
    add_to_cart(cart, {"id": "2", "name": "Fries", "price": 4.50, "quantity": 2})
    customer = {"name": "Gaber", "address": "123 Main St"}

    expected_cart_total = 10.00 * 1 + 4.50 * 2

    placed = place_order(cart, customer)
    confirmation = get_confirmation(placed["order_id"])

    assert confirmation["total"] == expected_cart_total


# INTEGRATION: Cart + Order Placement
def test_empty_cart_place_order_returns_cart_empty_error():
    cart = []  # add_to_cart never called — cart stays empty
    customer = {"name": "Gaber", "address": "123 Main St"}

    result = place_order(cart, customer)

    assert result["error"] == "Cart is empty"
