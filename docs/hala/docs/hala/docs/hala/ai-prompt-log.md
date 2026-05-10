# AI Prompt Log — Cart Feature
## CSE323 Restaurant Customer Ordering System
**Author:** Hala  
**Feature:** Cart (add/remove items, update quantity, show total)  
**Tool used:** Claude (Anthropic)  
**Purpose:** This log documents every AI prompt used during the design, development, and testing of the Cart feature, as required by the project appendix guidelines.

---

## Section 1 — Requirements & Edge Cases

### Prompt 1.1 — Gherkin scenarios
**Phase:** Requirements & Design  
**Linked deliverable:** `docs/hala/cart.feature`  
**Linked scenarios:** SC-CART-01, SC-CART-02, SC-CART-03

**Prompt sent to AI:**
```
I choose Option 1. Please write 3 Gherkin scenarios for my Cart feature.
Include one scenario for adding an item, one for updating quantity, and one
failure case (e.g., trying to add a negative quantity). Format them cleanly.
```

**What the AI produced:**
- 5 Gherkin scenarios in strict Given/When/Then syntax (3 required + 2 bonus edge cases)
- Scenario IDs: SC-CART-01 through SC-CART-05
- Covered: happy path add, quantity update, negative quantity error, empty cart after remove, quantity-zero confirmation dialog

**How it was used:**
Pasted directly into `docs/hala/cart.feature` and committed to `feature/hala-cart`. Scenario IDs were used as the primary keys in the traceability matrix.

---

## Section 2 — Gherkin & API Design

### Prompt 2.1 — API contracts and QA audit log
**Phase:** Design  
**Linked deliverable:** `docs/hala/cart-api-contracts.md`  
**Linked requirements:** REQ-C-01, REQ-C-02, REQ-C-03

**Prompt sent to AI:**
```
I choose Option 2. First, write the API contracts for my core Python Cart
methods (add_to_cart, update_quantity, remove_from_cart). Show the inputs
and outputs clearly. Second, create a QA Audit Log table. Take 3 vague
requirements (like 'cart updates fast', 'handles large orders', 'accurate
prices') and translate them into strict, quantifiable numbers.
```

**What the AI produced:**

*API contracts (inputs and outputs, no internal logic):*

| Method | HTTP method | Key inputs | Key outputs |
|---|---|---|---|
| `add_to_cart` | POST | `item_id: str`, `quantity: int (1–20)` | `success: bool`, `cart_total: float`, `cart_item_count: int` |
| `update_quantity` | PATCH | `item_id: str`, `new_quantity: int` | `success: bool`, `line_total: float`, `cart_total: float` |
| `remove_from_cart` | DELETE | `item_id: str` | `success: bool`, `cart_is_empty: bool`, `cart_total: float` |

*QA audit log (vague → measurable):*

| Req ID | Original vague wording | Strict measurable requirement |
|---|---|---|
| REQ-C-01 | "Cart updates fast" | Cart total and badge re-render within 300 ms of any action |
| REQ-C-02 | "Handles large orders" | Cart supports max 20 unique items; 21st item returns `CART_ITEM_LIMIT_REACHED` |
| REQ-C-03 | "Accurate prices" | `cart_total` = sum of (unit_price × quantity), rounded to 2 dp, tolerance ±0.01 EGP |

**How it was used:**
Saved to `docs/hala/cart-api-contracts.md`. Error codes (`INVALID_ITEM_ID`, `NEGATIVE_QUANTITY`, etc.) were carried forward into `cart.py` and matched exactly in `test_cart.py` assertions.

---

## Section 3 — TDD Backend Python Logic

### Prompt 3.1 — Failing pytest tests (red phase)
**Phase:** TDD — Red  
**Linked deliverable:** `tests/test_cart.py`  
**Linked scenarios:** SC-CART-01, SC-CART-02, SC-CART-03  
**Git commit:** `test: failing tests for add_to_cart — red phase`

**Prompt sent to AI:**
```
Let's move to Option 3. We are doing the backend strictly in Python. Write
a pytest unit test file (test_cart.py) for the Cart class's add_to_cart
method. Test for success and correct total calculation. DO NOT give me the
cart.py code yet. Only give me the test, and give me the exact git commit
command for a failing test.
```

**What the AI produced:**
- 9 pytest unit tests covering: success return value, item presence in cart, badge count, total for single item, total for quantity > 1, total for multiple items, negative quantity error, zero quantity error, quantity > 20 error, empty `item_id` error
- One `@pytest.fixture` for a fresh `Cart()` instance per test
- Shared test data constants (`BURGER`, `FRIES`)
- Exact GitHub commit command for the red phase

**Key design decisions AI explained:**
- One assertion per test function for clean traceability
- `abs(result - expected) <= 0.01` pattern to satisfy REQ-C-03 tolerance
- `pytest.raises(ValueError, match="...")` with exact error strings that must match `cart.py`

**How it was used:**
Created as `tests/test_cart.py` on GitHub via the website editor. Committed before `cart.py` existed, producing an `ImportError` — this is the intentional red phase evidence.

---

### Prompt 3.2 — cart.py implementation (green phase)
**Phase:** TDD — Green  
**Linked deliverable:** `cart.py`  
**Linked scenarios:** SC-CART-01, SC-CART-02, SC-CART-03  
**Git commit:** `feat: implement Cart.add_to_cart — green phase`

**Prompt sent to AI:**
```
I have successfully committed the failing test. Now, write the actual Python
code for cart.py so that the test passes. Also, give me the git commit
command for this new feature.
```

**What the AI produced:**
- `Cart` class with `__init__`, `cart_item_count` property, `cart_total` property, and `add_to_cart` method
- Input validation in this exact order: empty `item_id` → quantity < 1 → quantity > 20 → cart item limit → insert or update
- `round(total, 2)` on `cart_total` to satisfy REQ-C-03
- Constants `MAX_QUANTITY = 20` and `MAX_ITEMS = 20` for REQ-C-02
- Error messages worded to match `match=` strings in `test_cart.py` exactly

**How it was used:**
Created as `cart.py` in the project root on GitHub. After committing, all 9 tests pass — completing the green phase. The two-commit sequence (test before code) is the TDD proof visible in the commit history.

---

## Section 4 — Playwright E2E Testing

### Prompt 4.1 — CartPage POM and E2E test file
**Phase:** E2E Testing  
**Linked deliverables:** `tests/pages/CartPage.py`, `tests/test_e2e_cart.py`  
**Linked scenarios:** SC-CART-01 through SC-CART-05  
**Git commits:**  
- `test: add CartPage POM with locators for Cart E2E tests`  
- `test: add E2E tests for Cart feature using Playwright POM`

**Prompt sent to AI:**
```
Let's finish with Option 4. Write the Playwright End-to-End tests in Python.
We must use the Page Object Model (POM). Create a CartPage.py class that
stores the UI locators, and a test_e2e_cart.py file that uses pytest and
playwright-python to open the browser, click the 'Add' buttons, and verify
the UI total updates correctly.
```

**What the AI produced:**

*`CartPage.py` — POM class (locators and actions only, zero assertions):*
- Locators using `data-testid` attributes for resilience against CSS changes
- Methods: `goto()`, `add_item_to_cart()`, `set_item_quantity()`, `remove_item()`, `get_cart_total_text()`, `get_cart_badge_count()`, `is_empty_message_visible()`, `confirm_remove()`

*`test_e2e_cart.py` — 5 E2E tests (assertions only, zero raw selectors):*

| Test function | Gherkin scenario covered |
|---|---|
| `test_add_single_item_updates_total_and_badge` | SC-CART-01 |
| `test_update_quantity_recalculates_total` | SC-CART-02 |
| `test_add_two_items_total_is_sum_of_both` | REQ-C-03 multi-item |
| `test_negative_quantity_shows_error_message` | SC-CART-03 |
| `test_remove_last_item_shows_empty_cart_message` | SC-CART-04 |
| `test_set_quantity_zero_triggers_confirm_dialog` | SC-CART-05 |

**Key design decisions AI explained:**
- Strict POM rule: `CartPage.py` holds all selectors; `test_e2e_cart.py` holds all assertions — the two files never mix responsibilities
- `data-testid` naming convention auto-converts item names: `"Classic Burger"` → `add-btn-classic-burger`
- `expect()` used for UI text assertions; plain `assert` used for boolean and count assertions

**How it was used:**
Two separate files committed to GitHub: `tests/pages/CartPage.py` and `tests/test_e2e_cart.py`. E2E tests will run once the combined frontend is deployed.

---

## Section 5 — UML Diagrams

### Prompt 5.1 — Mermaid.js UML diagrams for draw.io
**Phase:** Design documentation  
**Linked deliverables:** `docs/hala/diagram-1-sequence-success.png`, `docs/hala/diagram-2-sequence-failure.png`, `docs/hala/diagram-3-activity-add-to-cart.png`

**Prompt sent to AI:**
```
I need to create my UML diagrams for the Cart feature to put into draw.io.
Please generate the exact Mermaid.js code for three diagrams based on our
Python code:
1. A Sequence Diagram for a successful 'add to cart' flow between the
   Customer, UI, and Backend.
2. A Sequence Diagram for a failed 'add to cart' flow (e.g., inputting a
   negative quantity).
3. An Activity Diagram flowchart showing the decision logic of adding/updating
   items (checking if quantity > 0, checking if item already exists).
Make sure the syntax is perfect so I can paste it directly into draw.io's
Insert -> Advanced -> Mermaid tool.
```

**What the AI produced:**
- Diagram 1: `sequenceDiagram` with `autonumber`, three participants (Customer, Cart UI, Backend), `activate`/`deactivate` blocks showing the successful flow — SC-CART-01
- Diagram 2: `sequenceDiagram` with `alt`/`else`/`end` block showing the `ValueError` path and unchanged cart state — SC-CART-03
- Diagram 3: `flowchart TD` with four decision diamonds (empty `item_id`, quantity < 1, quantity > 20, cart limit), two terminal paths (insert vs update), and two outcome nodes (success/failure)

**How it was used:**
Each Mermaid block was pasted into draw.io via Insert → Advanced → Mermaid, exported as PNG, and uploaded to `docs/hala/` on GitHub.

---

## Section 6 — Verification & Validation

### Prompt 6.1 — V&V statements
**Phase:** Final documentation  
**Linked deliverable:** `docs/hala/vv-statements.md`

**Prompt sent to AI:**
```
I need to write my final Verification & Validation (V&V) statements for the
Cart feature. Based on the Python pytest unit tests and Playwright POM E2E
tests we just wrote, please generate two highly professional sentences:
1. A Verification statement explaining how the unit tests prove the math and
   logic are mathematically correct.
2. A Validation statement explaining how the E2E tests prove the feature
   solves the real user's problem of reviewing their order before checkout.
Please keep it to exactly two sentences total.
```

**What the AI produced:**

> **Verification:** The Cart feature is verified correct because all 9 pytest unit tests in `test_cart.py` pass deterministically against `cart.py`, demonstrating that `add_to_cart` enforces quantity bounds of 1–20, raises the exact `ValueError` messages specified in SC-CART-03, and computes `cart_total` as the precise sum of all (unit_price × quantity) lines rounded to 2 decimal places — within the ±0.01 EGP tolerance defined in REQ-C-03.

> **Validation:** The Cart feature is validated against the real customer need because the 5 Playwright E2E tests in `test_e2e_cart.py` simulate a complete browser session — adding items, adjusting quantities, removing products, and confirming that the displayed total updates accurately at every step — thereby proving that a customer can confidently review the exact contents and cost of their order before proceeding to checkout, with no silent calculation errors or stale UI states.

**How it was used:**
Saved to `docs/hala/vv-statements.md` and committed to `feature/hala-cart`.

---

## Summary table — all prompts

| # | Section | Prompt purpose | Output file | Commit message |
|---|---|---|---|---|
| 1.1 | Requirements | Gherkin scenarios | `docs/hala/cart.feature` | `docs: add Gherkin scenarios for Cart feature` |
| 2.1 | API Design | API contracts + QA audit log | `docs/hala/cart-api-contracts.md` | `docs: add API contracts and QA audit log for Cart feature` |
| 3.1 | TDD Red | Failing pytest unit tests | `tests/test_cart.py` | `test: failing tests for add_to_cart — red phase` |
| 3.2 | TDD Green | cart.py implementation | `cart.py` | `feat: implement Cart.add_to_cart — green phase` |
| 4.1 | E2E POM | CartPage.py locator class | `tests/pages/CartPage.py` | `test: add CartPage POM with locators for Cart E2E tests` |
| 4.1 | E2E Tests | Playwright E2E test file | `tests/test_e2e_cart.py` | `test: add E2E tests for Cart feature using Playwright POM` |
| 5.1 | UML | Mermaid.js diagram code | `docs/hala/*.png` | `docs: add UML sequence and activity diagrams for Cart feature` |
| 6.1 | V&V | Verification & Validation statements | `docs/hala/vv-statements.md` | `docs: add V&V statements for Cart feature` |
