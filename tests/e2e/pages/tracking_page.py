"""Page Object Model for the Order Tracking UI.

SHELL ONLY — to be implemented by Amr (Tracking feature owner).

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


class TrackingPage:
    """Page object for the order tracking page."""

    INDEX_URL = f"{BASE_URL}/track"

    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def goto_index(self):
        """Navigate to the tracking landing page."""
        self.page.goto(self.INDEX_URL)
        return self

    def goto_order(self, order_id: str):
        """Navigate to the tracking page for a specific order."""
        self.page.goto(f"{BASE_URL}/track/{order_id}")
        return self

    # ------------------------------------------------------------------
    # TODO: locators (e.g. status_badge, estimated_delivery, order_id_display)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # TODO: actions (e.g. refresh_status, lookup_by_id)
    # ------------------------------------------------------------------
