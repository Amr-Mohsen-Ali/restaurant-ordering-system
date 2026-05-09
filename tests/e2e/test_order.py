"""Playwright E2E tests for the Order Placement feature.

One test function per Gherkin scenario. Tests are organised in a single class
that mirrors the OrderPage page object — each describe-style class corresponds
to one feature/page object.

Prerequisites:
- The Flask app must be running on http://127.0.0.1:5000 (run `python app.py`).
- pytest-playwright must be installed and browsers downloaded:
      pip install pytest-playwright
      playwright install chromium

Run from project root:
      pytest tests/e2e/test_order.py -v
"""

from playwright.sync_api import Page, expect

from tests.e2e.pages.order_page import OrderPage


class TestOrderPlacement:
    """E2E coverage for Gaber's Order Placement feature.

    Maps to the three Gherkin scenarios documented in docs/gherkin.md.
    """

    # ------------------------------------------------------------------
    # Scenario 1 — Customer places a valid order
    #
    #   Given the customer is on the checkout page with items in the cart
    #   When they fill in name and address and click Place Order
    #   Then they see a confirmation screen with an order ID and estimated time
    # ------------------------------------------------------------------

    def test_customer_places_a_valid_order(self, page: Page):
        order_page = OrderPage(page)
        order_page.goto_checkout()
        order_page.submit_order(name="Gaber", address="123 Main St")

        # The Gherkin Then is compound: an order ID AND estimated time.
        # Both must be present on the confirmation screen.
        expect(order_page.order_id_row).to_contain_text("ORD-")
        expect(order_page.estimated_time_row).to_contain_text("25")

    # ------------------------------------------------------------------
    # Scenario 2 — Customer tries to place an order with empty cart
    #
    #   Given the customer is on the checkout page with empty cart
    #   When they see the Place Order button
    #   Then the button is disabled
    # ------------------------------------------------------------------

    def test_place_order_button_is_disabled_when_cart_is_empty(self, page: Page):
        order_page = OrderPage(page)
        order_page.goto_empty_checkout()

        expect(order_page.place_order_button).to_be_disabled()

    # ------------------------------------------------------------------
    # Scenario 3 — Order placement fails due to missing customer info
    #
    #   Given the customer is on the checkout page with items in the cart
    #   When they click Place Order without filling name or address
    #   Then they see an error message saying Missing customer info
    # ------------------------------------------------------------------

    def test_order_fails_with_missing_customer_info(self, page: Page):
        order_page = OrderPage(page)
        order_page.goto_checkout()
        order_page.click_place_order()

        expect(order_page.error_message("Missing customer info")).to_be_visible()
