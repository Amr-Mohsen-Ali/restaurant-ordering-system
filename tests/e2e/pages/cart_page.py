"""Page Object Model for the Cart UI.

SHELL ONLY — to be implemented by the Cart feature owner.

Pattern to follow (see order_page.py for the worked example):
- Add URL constants for the page's routes.
- Add `@property` locators using accessibility-first selectors
  (get_by_role / get_by_label / get_by_text) where possible.
- Add action methods (clicks, form fills) that return `self` for chaining.
- Keep all selectors inside this class — tests should never reach into
  the DOM directly.
"""

from playwright.sync_api import Page


BASE_URL = "http://127.0.0.1:5000"


class CartPage:
    """Page object for the cart page."""

    URL = f"{BASE_URL}/cart"

    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def goto(self):
        self.page.goto(self.URL)
        return self

    # ------------------------------------------------------------------
    # TODO: locators (e.g. cart_items, total_amount, checkout_link)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # TODO: actions (e.g. remove_item, update_quantity, proceed_to_checkout)
    # ------------------------------------------------------------------
