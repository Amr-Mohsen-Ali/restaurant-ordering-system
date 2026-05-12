# Cart Feature — Hala

## What this feature does
Allows the customer to add menu items to a cart, update quantities,
remove items, and see a live running total before placing an order.

## Files I own

| File | Purpose |
|---|---|
| `cart.py` | Core Cart class with all business logic |
| `tests/test_cart.py` | 9 pytest unit tests — TDD red/green evidence |
| `tests/pages/CartPage.py` | Playwright Page Object Model — all locators |
| `tests/test_e2e_cart.py` | 5 Playwright E2E tests — one per Gherkin scenario |

## Documentation in this folder

| File | Contents |
|---|---|
| `cart.feature` | 5 Gherkin scenarios (SC-CART-01 to SC-CART-05) |
| `cart-api-contracts.md` | API contracts + QA audit log |
| `vv-statements.md` | Verification & Validation statements |
| `ai-prompt-log.md` | All AI prompts used — appendix evidence |
| `integration-guide.md` | How teammates connect to my Cart module |
| `diagram-1-sequence-success.png` | UML sequence diagram — happy path |
| `diagram-2-sequence-failure.png` | UML sequence diagram — error path |
| `diagram-3-activity-add-to-cart.png` | UML activity diagram — decision logic |

## My TDD commit evidence

| Commit message | Phase | What it proves |
|---|---|---|
| `test: failing tests for add_to_cart — red phase` | Red | Test written before code |
| `feat: implement Cart.add_to_cart — green phase` | Green | Code written to pass tests |

## Requirements I own

| Req ID | Requirement | Status |
|---|---|---|
| REQ-C-01 | Cart updates within 300 ms | Done |
| REQ-C-02 | Max 20 unique items in cart | Done |
| REQ-C-03 | Total accurate to ±0.01 EGP | Done |
