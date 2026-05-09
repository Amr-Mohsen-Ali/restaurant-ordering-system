# Cart Feature — API Contracts & QA Audit Log

## API Contracts

### addToCart(itemId, quantity) — POST

**Input:**
| Field    | Type    | Constraints         |
|----------|---------|---------------------|
| itemId   | string  | must be a valid ID  |
| quantity | integer | min: 1, max: 20     |

**Output (success):**
```json
{
  "success": true,
  "cartItemCount": 2,
  "cartTotal": 150.00,
  "addedItem": {
    "itemId": "item_042",
    "name": "Classic Burger",
    "quantity": 1,
    "unitPrice": 75.00
  }
}
```

**Error codes:** INVALID_ITEM_ID | QUANTITY_OUT_OF_RANGE | ITEM_UNAVAILABLE

---

### updateQuantity(itemId, newQuantity) — PATCH

**Input:**
| Field       | Type    | Constraints                  |
|-------------|---------|------------------------------|
| itemId      | string  | must exist in cart           |
| newQuantity | integer | 0 triggers remove confirm    |

**Output (success):**
```json
{
  "success": true,
  "updatedItem": {
    "itemId": "item_042",
    "newQuantity": 3,
    "lineTotal": 225.00
  },
  "cartTotal": 225.00,
  "cartItemCount": 3
}
```

**Error codes:** ITEM_NOT_IN_CART | NEGATIVE_QUANTITY | QUANTITY_EXCEEDS_MAX

---

### removeFromCart(itemId) — DELETE

**Input:**
| Field  | Type   | Constraints        |
|--------|--------|--------------------|
| itemId | string | must exist in cart |

**Output (success):**
```json
{
  "success": true,
  "removedItemId": "item_042",
  "cartTotal": 0.00,
  "cartItemCount": 0,
  "cartIsEmpty": true
}
```

**Error codes:** ITEM_NOT_IN_CART | CART_ALREADY_EMPTY

---
## QA Audit Log

| Req ID   | Original vague wording              | Strict measurable requirement                                                                                      | How to test                                      | Linked scenario          |
|----------|-------------------------------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|--------------------------|
| REQ-C-01 | "The cart should update fast"       | Cart total and item count must re-render within 300 ms of any add/update/remove action                             | Jest: mock Date.now(); Playwright: waitForFunction | SC-CART-01, SC-CART-02  |
| REQ-C-02 | "The cart should hold a lot of items" | Cart supports max 20 unique items. A 21st item returns CART_ITEM_LIMIT_REACHED and shows "Cart is full (20 items max)" | Jest: loop addToCart 21×, assert error on 21st  | SC-CART-04              |
| REQ-C-03 | "The total price should always be correct" | Cart total = sum of (unitPrice × quantity) per item, rounded to 2 decimal places. Tolerance: ±0.01 EGP            | Jest: add 3 items, assert cartTotal within ±0.01 | SC-CART-01, SC-CART-02, SC-CART-05 |
