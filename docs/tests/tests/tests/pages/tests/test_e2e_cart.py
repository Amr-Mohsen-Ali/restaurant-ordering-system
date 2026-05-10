# tests/test_e2e_cart.py
# E2E layer — 10% of test suite as per project spec.
# Uses CartPage POM exclusively — zero raw selectors here.
# Each test = one Gherkin scenario converted to Playwright.

import pytest
from playwright.sync_api import Page, expect
from tests.pages.CartPage import CartPage


# ── fixture: fresh CartPage for every test ─────────────────────

@pytest.fixture
def cart(page: Page) -> CartPage:
    """
    Navigate to the app and return a CartPage instance.
    Playwright's built-in 'page' fixture handles browser lifecycle.
    """
    cart_page = CartPage(page)
    cart_page.goto()
    return cart_page


# ── SC-CART-01: add a single item ──────────────────────────────

def test_add_single_item_updates_total_and_badge(cart: CartPage):
    """
    Gherkin SC-CART-01:
      Given the customer is on the menu page and the cart is empty
      When  they click Add on Classic Burger (EGP 75.00)
      Then  the cart total shows EGP 75.00 and badge shows 1
    """
    cart.add_item_to_cart("Classic Burger")

    expect(cart.cart_total).to_have_text("EGP 75.00")
    assert cart.get_cart_badge_count() == 1


# ── SC-CART-02: update quantity recalculates total ─────────────

def test_update_quantity_recalculates_total(cart: CartPage):
    """
    Gherkin SC-CART-02:
      Given the customer has 1 Classic Burger in the cart
      When  they change the quantity to 3
      Then  the cart total shows EGP 225.00 and badge shows 3
    """
    cart.add_item_to_cart("Classic Burger")
    cart.set_item_quantity("Classic Burger", 3)

    expect(cart.cart_total).to_have_text("EGP 225.00")
    assert cart.get_cart_badge_count() == 3


# ── SC-CART-02 extended: multi-item total ─────────────────────

def test_add_two_items_total_is_sum_of_both(cart: CartPage):
    """
    REQ-C-03: total = sum of all (unit_price × qty) lines.
      Classic Burger × 2 = EGP 150.00
      Fries          × 1 = EGP  30.00
      Expected total     = EGP 180.00
    """
    cart.add_item_to_cart("Classic Burger")
    cart.set_item_quantity("Classic Burger", 2)
    cart.add_item_to_cart("Fries")

    expect(cart.cart_total).to_have_text("EGP 180.00")


# ── SC-CART-03: negative quantity shows error ──────────────────

def test_negative_quantity_shows_error_message(cart: CartPage):
    """
    Gherkin SC-CART-03:
      Given 1 Classic Burger in cart
      When  quantity is set to -1
      Then  error 'Quantity must be at least 1' is shown
      And   the total is unchanged
    """
    cart.add_item_to_cart("Classic Burger")
    cart.set_item_quantity("Classic Burger", -1)

    assert "Quantity must be at least 1" in cart.get_error_message_text()
    expect(cart.cart_total).to_have_text("EGP 75.00")  # unchanged


# ── SC-CART-04: remove last item shows empty state ─────────────

def test_remove_last_item_shows_empty_cart_message(cart: CartPage):
    """
    Gherkin SC-CART-04:
      Given 1 Classic Burger in cart
      When  the customer clicks remove
      Then  'Your cart is empty' message appears
      And   cart total shows EGP 0.00
      And   cart badge is hidden
    """
    cart.add_item_to_cart("Classic Burger")
    cart.remove_item("Classic Burger")

    assert cart.is_empty_message_visible()
    expect(cart.cart_total).to_have_text("EGP 0.00")
    assert not cart.is_cart_badge_visible()


# ── SC-CART-05: qty=0 triggers remove confirmation ────────────

def test_set_quantity_zero_triggers_confirm_dialog(cart: CartPage):
    """
    Gherkin SC-CART-05:
      Given 2 Fries in cart
      When  quantity is set to 0
      Then  a confirmation dialog 'Remove Fries from cart?' appears
      And   after confirming, cart is empty
    """
    cart.add_item_to_cart("Fries")
    cart.set_item_quantity("Fries", 2)
    cart.set_item_quantity("Fries", 0)

    assert cart.is_remove_confirm_visible()
    cart.confirm_remove()
    assert cart.is_empty_message_visible()
