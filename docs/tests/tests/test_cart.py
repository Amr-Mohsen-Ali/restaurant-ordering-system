# tests/test_cart.py
# TDD Step 1 — these tests MUST fail before cart.py exists.
# Linked requirements: REQ-C-01, REQ-C-03 | Scenarios: SC-CART-01, SC-CART-02, SC-CART-03

import pytest
from cart import Cart  # ← ImportError expected — cart.py does not exist yet


# ─────────────────────────────────────────────
#  Shared test data
# ─────────────────────────────────────────────

BURGER = {"item_id": "item_001", "name": "Classic Burger", "unit_price": 75.00}
FRIES  = {"item_id": "item_002", "name": "Fries",          "unit_price": 30.00}


# ─────────────────────────────────────────────
#  Fixture — fresh cart before every test
# ─────────────────────────────────────────────

@pytest.fixture
def empty_cart():
    """Returns a brand-new Cart instance for each test."""
    return Cart()


# ─────────────────────────────────────────────
#  SC-CART-01 — Happy path: add one item
# ─────────────────────────────────────────────

def test_add_single_item_returns_success(empty_cart):
    """add_to_cart returns success=True when a valid item is added."""
    result = empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert result["success"] is True


def test_add_single_item_appears_in_cart(empty_cart):
    """Item is present in cart items after add_to_cart."""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert BURGER["item_id"] in empty_cart.items


def test_add_single_item_cart_count_is_one(empty_cart):
    """cart_item_count == 1 after adding one item with quantity 1."""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert empty_cart.cart_item_count == 1


# ─────────────────────────────────────────────
#  SC-CART-01 + REQ-C-03 — Total calculation
# ─────────────────────────────────────────────

def test_cart_total_equals_unit_price_for_single_item(empty_cart):
    """cart_total == unit_price when quantity is 1. (REQ-C-03: tolerance ±0.01 EGP)"""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert abs(empty_cart.cart_total - 75.00) <= 0.01


# ─────────────────────────────────────────────
#  SC-CART-02 — Total recalculates for quantity > 1
# ─────────────────────────────────────────────

def test_cart_total_multiplies_by_quantity(empty_cart):
    """cart_total == unit_price × quantity for a single item type."""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=3)

    assert abs(empty_cart.cart_total - 225.00) <= 0.01  # 75.00 × 3


def test_cart_total_sums_multiple_items(empty_cart):
    """cart_total == sum of all (unit_price × quantity) lines. (REQ-C-03)"""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=2)
    empty_cart.add_to_cart(FRIES["item_id"],  FRIES["unit_price"],  quantity=1)

    expected = (75.00 * 2) + (30.00 * 1)  # = 180.00
    assert abs(empty_cart.cart_total - expected) <= 0.01


# ─────────────────────────────────────────────
#  SC-CART-03 — Wrong path: invalid inputs
# ─────────────────────────────────────────────

def test_add_negative_quantity_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for quantity < 1. (SC-CART-03)"""
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=-1)


def test_add_zero_quantity_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for quantity == 0."""
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=0)


def test_add_exceeds_max_quantity_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for quantity > 20. (REQ-C-02)"""
    with pytest.raises(ValueError, match="Quantity must not exceed 20"):
        empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=21)


def test_add_empty_item_id_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for blank item_id."""
    with pytest.raises(ValueError, match="item_id must not be empty"):
        empty_cart.add_to_cart("", BURGER["unit_price"], quantity=1)
