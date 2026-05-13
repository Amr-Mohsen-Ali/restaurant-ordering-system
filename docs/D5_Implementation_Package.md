# D5 - Implementation Package

## 1. Project Information

| Field | Value |
|-------|-------|
| **Project Name** | Restaurant Ordering System |
| **Sub-system** | Customer Ordering System |
| **GitHub Repository** | https://github.com/Amr-Mohsen-Ali/restaurant-ordering-system |
| **Demo Video Link** | [To be added by student] |

---

## 2. TDP Evidence (Test-Driven Development)

### 2.1 TDP Iteration 1: Menu Feature

**Prompt:** "Write failing tests for menu filtering and category display"

**Failing Test Output:**
```
FAILED tests/test_menu.py::test_menu_filter_by_category - AssertionError: assert [] == ['Main']
```

**After Implementation:**
```
PASSED tests/test_menu.py::test_menu_filter_by_category
```

**Code Changes:**
- Added category filtering in `src/menu.py`
- Created API endpoint `/api/menu?category=`

---

### 2.2 TDP Iteration 2: Cart Feature

**Prompt:** "Write failing tests for cart quantity limits and total calculation"

**Failing Test Output:**
```
FAILED tests/test_cart.py::test_add_exceeds_max_quantity_raises_value_error - AssertionError: assert 'Quantity must not exceed 20' in 'None'
```

**After Implementation:**
```
PASSED tests/test_cart.py::test_add_exceeds_max_quantity_raises_value_error
```

**Code Changes:**
- Implemented Cart class with MAX_QUANTITY = 20
- Added validation in `add_to_cart()` method
- Implemented total calculation with 2 decimal precision

---

### 2.3 TDP Iteration 3: Order Placement

**Prompt:** "Write failing tests for order placement with validation"

**Failing Test Output:**
```
FAILED tests/test_order.py::test_place_order_with_empty_items_returns_cart_empty_error - assert 201 == 400
```

**After Implementation:**
```
PASSED tests/test_order.py::test_place_order_with_empty_items_returns_cart_empty_error
```

**Code Changes:**
- Added cart empty validation
- Added customer info validation
- Implemented order ID generation

---

### 2.4 TDP Iteration 4: Tracking Feature

**Prompt:** "Write failing tests for order tracking status progression"

**Failing Test Output:**
```
FAILED tests/test_tracking.py::test_api_returns_status_for_valid_order - KeyError: 'status'
```

**After Implementation:**
```
PASSED tests/test_tracking.py::test_api_returns_status_for_valid_order
```

**Code Changes:**
- Created tracking API endpoint
- Implemented status progression (Preparing → Out for Delivery → Delivered)
- Added status advancement endpoint

---

## 3. Vertical Slice Demo

### 3.1 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)                   │
│  ├── templates/ (menu.html, cart.html, checkout.html)      │
│  ├── static/js/ (menu.js, cart.js, tracking.js)             │
│  └── static/css/ (style.css)                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask)                          │
│  ├── src/__init__.py (app factory)                         │
│  ├── src/menu.py (menu blueprint)                          │
│  ├── src/cart.py (cart blueprint)                          │
│  ├── src/order.py (order blueprint)                        │
│  └── src/tracking.py (tracking blueprint)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│  ├── src/data/orders.py (ORDERS dict)                      │
│  └── In-memory storage                                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Working Vertical Slice

| Layer | Delivery | Status |
|-------|----------|--------|
| **UI** | HTML templates with CSS styling | ✅ Working |
| **Logic** | Flask routes and business logic | ✅ Working |
| **Data** | In-memory order and cart storage | ✅ Working |

### 3.3 Failure Resilience

| Scenario | Handling | Status |
|----------|----------|--------|
| Empty cart order | Returns 400 with error message | ✅ |
| Invalid order ID | Returns 404 with error message | ✅ |
| Invalid quantity | Returns 400 with error message | ✅ |
| Network timeout | Client shows error message | ✅ |

---

## 4. Source Code Structure

```
restaurant-ordering-system/
├── src/
│   ├── __init__.py          # Flask app factory
│   ├── menu.py              # Menu feature
│   ├── cart.py              # Cart feature (includes Cart class)
│   ├── order.py             # Order placement
│   ├── tracking.py          # Order tracking
│   └── data/
│       └── orders.py        # Shared order storage
├── templates/               # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── menu.html
│   ├── cart.html
│   ├── checkout.html
│   └── tracking.html
├── static/
│   ├── css/style.css       # Global styles
│   └── js/                 # Frontend JS
│       ├── menu.js
│       ├── cart.js
│       └── tracking.js
├── tests/                   # Test suite (90 tests)
├── docs/                    # Documentation
│   ├── D2_Requirements_Report.md
│   ├── D3_Design_Specification.md
│   └── D4_Validation_Report.md
└── README.md
```

---

## 5. Running the Application

### 5.1 Prerequisites
```bash
pip install flask pytest playwright
```

### 5.2 Start Application
```bash
python app.py
# Open http://127.0.0.1:5000
```

### 5.3 Run Tests
```bash
pytest tests/ -v
```

---

## 6. GitHub Commit History

| Commit | Description |
|--------|-------------|
| ae39493 | Integrate all features: Menu->Cart->Checkout->Tracking flow |
| 6549ab9 | Merge feature/amr-tracking into main |
| 328baa4 | Merge feature/gaber-order into main |
| 7f9798b | Merge branch 'feature/hala-cart' |
| 855c0f3 | feat: add Cart class and comprehensive tests |
| 1739ffd | feat: implement menu browsing with filtering |

---

## 7. Demo Video Recording

**Recording Required:** ≤ 5 minutes  
**Content should include:**
1. Browse menu and filter by category
2. Add items to cart
3. Proceed to checkout
4. Place order
5. Track order status
6. Advance order status (demo feature)

**Link:** [To be added by student]

---

*Document Version: 1.0*  
*Date: [Current Date]*  
*Sub-system: Customer Ordering System*