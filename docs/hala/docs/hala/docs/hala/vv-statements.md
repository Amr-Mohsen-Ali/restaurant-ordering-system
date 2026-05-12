# Verification & Validation Statements — Cart Feature

## Verification
The Cart feature is verified correct because all 9 pytest unit tests in
`test_cart.py` pass deterministically against `cart.py`, demonstrating
that `add_to_cart` enforces quantity bounds of 1–20, raises the exact
`ValueError` messages specified in SC-CART-03, and computes `cart_total`
as the precise sum of all (unit_price × quantity) lines rounded to
2 decimal places — within the ±0.01 EGP tolerance defined in REQ-C-03.

## Validation
The Cart feature is validated against the real customer need because the
5 Playwright E2E tests in `test_e2e_cart.py` simulate a complete browser
session — adding items, adjusting quantities, removing products, and
confirming that the displayed total updates accurately at every step —
thereby proving that a customer can confidently review the exact contents
and cost of their order before proceeding to checkout, with no silent
calculation errors or stale UI states.
