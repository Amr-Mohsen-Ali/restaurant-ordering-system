"""Page Object Model for the Order Placement / Checkout UI.

Encapsulates locators and user actions for:
- the cart view (form + Place Order button)
- the confirmation view (order ID, items, total, estimated time, Cancel button)
- the cancelled view
- the error view

All selectors use Playwright's accessibility-first locators (get_by_role,
get_by_label, get_by_text) where possible. CSS class selectors are used only
where the DOM has no semantic role for the target element.
"""

from playwright.sync_api import Page


BASE_URL = "http://127.0.0.1:5000"


class OrderPage:
    """Page object for the Order Placement / Checkout flow."""

    CHECKOUT_URL = f"{BASE_URL}/checkout"
    EMPTY_CHECKOUT_URL = f"{BASE_URL}/checkout?empty=1"

    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def goto_checkout(self):
        """Navigate to the checkout page with the demo cart populated."""
        self.page.goto(self.CHECKOUT_URL)
        return self

    def goto_empty_checkout(self):
        """Navigate to the checkout page in empty-cart demo mode."""
        self.page.goto(self.EMPTY_CHECKOUT_URL)
        return self

    # ------------------------------------------------------------------
    # Form interactions
    # ------------------------------------------------------------------

    def fill_name(self, name: str):
        self.name_input.fill(name)
        return self

    def fill_address(self, address: str):
        self.address_input.fill(address)
        return self

    def click_place_order(self):
        self.place_order_button.click()
        return self

    def submit_order(self, name: str, address: str):
        """Compound action: fill the form and click Place Order."""
        self.fill_name(name)
        self.fill_address(address)
        self.click_place_order()
        return self

    # ------------------------------------------------------------------
    # Confirmation-view interactions
    # ------------------------------------------------------------------

    def click_cancel_order(self):
        self.cancel_order_button.click()
        return self

    # ------------------------------------------------------------------
    # Locators (cart view)
    # ------------------------------------------------------------------

    @property
    def name_input(self):
        return self.page.get_by_label("Name")

    @property
    def address_input(self):
        return self.page.get_by_label("Address")

    @property
    def place_order_button(self):
        return self.page.get_by_role("button", name="Place Order")

    @property
    def cart_error_alert(self):
        """Inline error banner shown on the cart view when placeOrder fails."""
        return self.page.locator(".alert-error")

    # ------------------------------------------------------------------
    # Locators (confirmation view)
    # ------------------------------------------------------------------

    @property
    def confirmation_heading(self):
        return self.page.get_by_role("heading", name="Order Confirmed")

    @property
    def order_id_row(self):
        """The <p> row labelled 'Order ID:' on the confirmation page."""
        return self.page.locator(".meta-row").filter(has_text="Order ID")

    @property
    def estimated_time_row(self):
        """The <p> row labelled 'Estimated time:' on the confirmation page."""
        return self.page.locator(".meta-row").filter(has_text="Estimated time")

    @property
    def status_row(self):
        return self.page.locator(".meta-row").filter(has_text="Status")

    @property
    def cancel_order_button(self):
        return self.page.get_by_role("button", name="Cancel Order")

    # ------------------------------------------------------------------
    # Locators (cancelled view)
    # ------------------------------------------------------------------

    @property
    def cancelled_heading(self):
        return self.page.get_by_role("heading", name="Order Cancelled")

    # ------------------------------------------------------------------
    # Locators (error view — for unknown order_id navigation)
    # ------------------------------------------------------------------

    @property
    def error_heading(self):
        return self.page.get_by_role("heading", name="Something went wrong")

    # ------------------------------------------------------------------
    # Text-content locators (used by error-message assertions)
    # ------------------------------------------------------------------

    def error_message(self, text: str):
        """Locator for an inline error banner containing the given text."""
        return self.page.locator(".alert-error").filter(has_text=text)
