# tests/pages/CartPage.py
# Page Object Model — ALL locators and UI actions live here.
# The test file NEVER touches raw selectors.
# Linked scenarios: SC-CART-01, SC-CART-02, SC-CART-03, SC-CART-04

from playwright.sync_api import Page, Locator


class CartPage:
    """
    Encapsulates every UI interaction for the Cart feature.
    One class per page — strictly no assertions inside this class.
    """

    URL = "http://localhost:3000"  # update when deployed

    # ── constructor ────────────────────────────────────────────────
    def __init__(self, page: Page):
        self.page = page

        # ── locators (data-testid attributes are the safest selectors) ─
        self.cart_total:       Locator = page.get_by_test_id("cart-total")
        self.cart_badge:       Locator = page.get_by_test_id("cart-badge")
        self.empty_message:    Locator = page.get_by_test_id("cart-empty-message")
        self.error_message:    Locator = page.get_by_test_id("cart-error-message")
        self.remove_confirm:   Locator = page.get_by_test_id("remove-confirm-dialog")
        self.confirm_btn:      Locator = page.get_by_test_id("confirm-remove-btn")

    # ── navigation ────────────────────────────────────────────────
    def goto(self):
        """Navigate to the app and wait until the menu is visible."""
        self.page.goto(self.URL)
        self.page.wait_for_selector("[data-testid='menu-page']")

    # ── item-level actions ────────────────────────────────────────
    def add_item_to_cart(self, item_name: str):
        """Click the Add button for a specific menu item by name."""
        self.page \
            .get_by_test_id(f"add-btn-{item_name.lower().replace(' ', '-')}") \
            .click()

    def set_item_quantity(self, item_name: str, quantity: int):
        """Clear and type a new quantity for a cart item."""
        qty_input = self.page.get_by_test_id(
            f"qty-input-{item_name.lower().replace(' ', '-')}"
        )
        qty_input.triple_click()            # select all existing text
        qty_input.type(str(quantity))      # type new value
        qty_input.press("Tab")             # trigger onBlur / onChange

    def remove_item(self, item_name: str):
        """Click the remove (trash) button for a specific cart item."""
        self.page \
            .get_by_test_id(f"remove-btn-{item_name.lower().replace(' ', '-')}") \
            .click()

    # ── reader helpers ────────────────────────────────────────────
    def get_cart_total_text(self) -> str:
        """Return the raw text shown in the cart total element."""
        return self.cart_total.inner_text()

    def get_cart_badge_count(self) -> int:
        """Return the integer shown in the cart item-count badge."""
        return int(self.cart_badge.inner_text())

    def is_cart_badge_visible(self) -> bool:
        return self.cart_badge.is_visible()

    def is_empty_message_visible(self) -> bool:
        return self.empty_message.is_visible()

    def get_error_message_text(self) -> str:
        return self.error_message.inner_text()

    def is_remove_confirm_visible(self) -> bool:
        return self.remove_confirm.is_visible()

    def confirm_remove(self):
        """Click OK on the remove-confirmation dialog."""
        self.confirm_btn.click()
