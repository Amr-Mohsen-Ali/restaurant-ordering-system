# D3 - Design Specification

## 1. Gherkin Scripts (Behavior-Driven Development)

### 1.1 Menu Feature

```gherkin
Feature: Menu Browsing
  As a customer
  I want to browse the menu
  So that I can see available food items

  Scenario: View all menu items
    Given the restaurant has menu items
    When I navigate to the menu page
    Then I should see all available items

  Scenario: Filter menu by category
    Given the menu has items in "Main", "Side", "Dessert", "Drink" categories
    When I select "Main" category filter
    Then I should see only "Main" category items

  Scenario Outline: Item availability display
    Given an item "<item_name>" with availability "<is_available>"
    When I view the menu
    Then I should see "<item_name>" marked as "<status>"
    
    Examples:
      | item_name     | is_available | status        |
      | Caesar Salad  | false        | Not Available |
      | Cheeseburger  | true         | available     |
```

### 1.2 Cart Feature

```gherkin
Feature: Shopping Cart Management
  As a customer
  I want to manage my cart
  So that I can select items for order

  Scenario: Add item to cart
    Given I am on the menu page
    When I select quantity 2 of "Cheeseburger"
    And I click "Add to Cart"
    Then the item should be added to my cart
    And cart total should reflect the added items

  Scenario: Quantity exceeds maximum
    Given I want to order 25 units of an item
    When I enter quantity "25"
    Then the system should reject with error "Quantity must not exceed 20"

  Scenario: Cart maintains correct total
    Given my cart has "Burger" x 2 at $9.99 each
    When I view my cart
    Then the total should be $19.98
```

### 1.3 Order Placement Feature

```gherkin
Feature: Order Placement
  As a customer
  I want to place an order
  So that I can receive my food

  Scenario: Successfully place order
    Given my cart has items
    And I have provided name "Ahmed" and address "123 Main St"
    When I submit the order
    Then the order should be created
    And I should receive an order ID
    And the order status should be "Preparing"

  Scenario: Place order with empty cart
    Given my cart is empty
    When I try to place an order
    Then I should see error "Cart is empty"
    And the order should not be created

  Scenario: Place order without customer info
    Given my cart has items
    But I have not provided my name
    When I submit the order
    Then I should see error "Missing customer info"
```

### 1.4 Order Tracking Feature

```gherkin
Feature: Order Tracking
  As a customer
  I want to track my order status
  So that I know when my food will arrive

  Scenario: Track valid order
    Given I have order ID "123"
    When I search for my order
    Then I should see status "Preparing"
    And I should see order details

  Scenario: Track invalid order
    Given order ID "999" does not exist
    When I search for order "999"
    Then I should see error "Invalid order ID"
    And I should see HTTP 404

  Scenario: Advance order status
    Given my order has status "Preparing"
    When kitchen staff advances the status
    Then the order status should change to "Out for Delivery"

  Scenario Outline: Status progression
    Given an order with current status "<current>"
    When the status is advanced
    Then the new status should be "<next>"
    
    Examples:
      | current           | next               |
      | Preparing         | Out for Delivery   |
      | Out for Delivery  | Delivered          |
      | Delivered         | Delivered (no change) |
```

---

## 2. UML Diagrams

### 2.1 System Sequence Diagram (Happy Path)

```
┌──────────┐     ┌────────┐     ┌────────┐     ┌─────────┐     ┌──────────┐
│ Customer │     │  Menu  │     │  Cart  │     │  Order  │     │ Tracking │
└────┬─────┘     └───┬────┘     └───┬────┘     └───┬─────┘     └───┬──────┘
     │              │             │              │              │
     │ GET /menu   │             │              │              │
     │────────────>│             │              │              │
     │             │             │              │              │
     │ POST /cart/add             │              │              │
     │────────────────────────────>│              │              │
     │              │             │              │              │
     │ POST /checkout             │              │              │
     │──────────────────────────────────────────>│              │
     │              │             │              │              │
     │              │             │              │ GET /track/ID│
     │              │             │              │─────────────>│
     │              │             │              │              │
```

### 2.2 System Sequence Diagram (Failure Path)

```
┌──────────┐     ┌────────┐     ┌────────┐
│ Customer │     │  Cart  │     │  Order │
└────┬─────┘     └───┬────┘     └───┬─────┘
     │              │             │
     │ POST /cart/add (qty > 20) │
     │──────────────────────────>│
     │              │      400 Bad Request
     │<──────────────────────────│
     │   "Quantity must not exceed 20"
     │
     │ POST /checkout (empty cart)│
     │───────────────────────────>│
     │              │      400 Bad Request
     │<──────────────────────────│
     │   "Cart is empty"
```

### 2.3 Activity Diagram - Order Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Browse Menu │
└──────┬──────┘
       │
       ▼
┌─────────────┐     No     ┌─────────────┐
│ Add to Cart │───────────>│ Empty?      │
└──────┬──────┘            └──────┬──────┘
       │                          │
       │ Yes                     │
       ▼                          │
┌─────────────┐                  │
│ View Cart   │                  │
└──────┬──────┘                  │
       │                          │
       ▼                          │
┌─────────────┐     No     ┌──────┴──────┐
│ Proceed to   │───────────>│  End (Error)│
│ Checkout    │            └─────────────┘
└──────┬──────┘
       │
       ▼
┌─────────────┐     No     ┌─────────────┐
│ Enter Info  │───────────>│ Valid?      │
└──────┬──────┘            └──────┬──────┘
       │                          │
       │ Yes                     │
       ▼                          │
┌─────────────┐                  │
│ Place Order │                  │
└──────┬──────┘                  │
       │                          │
       ▼                          │
┌─────────────┐                  │
│  Get Order  │                  │
│      ID     │                  │
└──────┬──────┘                  │
       │                          │
       ▼                          │
┌─────────────┐                  │
│   Track     │                  │
│   Order     │                  │
└──────┬──────┘                  │
       │                          │
       ▼                          │
┌─────────────┐                  │
│    End      │                  │
└─────────────┘                  │
```

---

## 3. API Contracts

### 3.1 Menu API

| Endpoint | Method | Parameters | Response |
|----------|--------|------------|----------|
| `/menu` | GET | None | HTML page with menu items |
| `/api/menu` | GET | `category` (optional) | JSON: `{"items": [...]}` |

**Response Example:**
```json
{
  "items": [
    {
      "id": "1",
      "name": "Margherita Pizza",
      "price": 11.99,
      "category": "Main",
      "ingredients": ["Tomato", "Mozzarella", "Basil"],
      "available": true
    }
  ]
}
```

### 3.2 Cart API

| Endpoint | Method | Parameters | Response |
|----------|--------|------------|----------|
| `/cart` | GET | None | HTML page showing cart |
| `/cart/add` | POST | `item_id`, `item_name`, `price`, `quantity` | JSON: `{"success": true, "total": 19.98}` |
| `/cart/update` | POST | `item_id`, `action` (increase/decrease/remove) | JSON: `{"success": true, "total": 9.99}` |
| `/cart/data` | GET | None | JSON: `{"items": [...], "total": 19.98}` |

### 3.3 Order API

| Endpoint | Method | Parameters | Response |
|----------|--------|------------|----------|
| `/checkout` | GET | None | HTML checkout page |
| `/checkout` | POST | `name`, `address` | Redirect to confirmation |
| `/checkout/confirmation/<id>` | GET | order_id | HTML confirmation page |
| `/place-order` | POST | `items`, `total`, `customer` | JSON with order_id |

### 3.4 Tracking API

| Endpoint | Method | Parameters | Response |
|----------|--------|------------|----------|
| `/tracking` | GET | None | HTML tracking page |
| `/track/<order_id>` | GET | order_id | JSON: `{"success": true, "status": "Preparing", "order": {...}}` |
| `/track/<order_id>/status` | POST | `status` | JSON: `{"success": true, "status": "Out for Delivery"}` |
| `/track/<order_id>/advance` | POST | None | JSON: `{"success": true, "status": "Out for Delivery"}` |

---

## 4. QA Audit Log

| Original Term | Issue | Refined Metric | Justification |
|---------------|-------|----------------|----------------|
| "Fast delivery" | Vague - what is fast? | "Estimated time ≤ 30 minutes" | Quantifiable threshold |
| "Fresh food" | Subjective | "Order prepared within 2 minutes of confirmation" | Measurable time-based metric |
| "Best quality" | Undefined | "All ingredients within expiration date" | Checkable condition |
| "Secure" | Abstract | "Passwords hashed with bcrypt, sessions use secure cookies" | Technical implementation |
| "User-friendly" | Ambiguous | "Page loads in < 3 seconds, mobile responsive" | Performance + UX metrics |

---

## 5. Internal Stack Hidden

| Layer | Technology | Hidden From Client |
|-------|------------|-------------------|
| Database | Python dict (in-memory) | ✅ Yes - exposed via API only |
| Business Logic | Flask Python | ✅ Yes - only JSON responses |
| Order Storage | `src/data/orders.py` | ✅ Yes - not exposed |
| Cart Storage | `src/cart.py` | ✅ Yes - API only |

---

*Document Version: 1.0*  
*Date: [Current Date]*  
*Sub-system: Customer Ordering System*