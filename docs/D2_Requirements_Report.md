# D2 - Requirements Report

## 1. Project Overview

**Project Name:** Restaurant Ordering System  
**Sub-system:** Customer Ordering System  
**Group Members:** [To be filled by student]

---

## 2. Actor Classification

### 2.1 Primary Actors (Directly use the system)

| Actor | Description | Use Case |
|-------|-------------|----------|
| **Customer** | End-user who browses menu, adds items to cart, places orders, and tracks delivery | Browse menu, Add to cart, Place order, Track order |
| **Guest User** | Unregistered user who can browse menu but cannot track orders | Browse menu, View prices |

### 2.2 Supporting Actors (Provide services to primary)

| Actor | Description | Use Case |
|-------|-------------|----------|
| **Kitchen Staff** | Receives orders for preparation | View new orders, Update order status |
| **Delivery Driver** | Delivers orders to customers | Update delivery status |

### 2.3 Offstage Actors (Indirectly affected)

| Actor | Description | Use Case |
|-------|-------------|----------|
| **Restaurant Manager** | Monitors order statistics and system performance | View analytics, Manage menu |
| **System Administrator** | Maintains system availability | Monitor system health |

---

## 3. Traceability Heatmap

### Requirements Matrix

| Feature | Requirement ID | Description | Test Coverage | Status |
|---------|---------------|-------------|---------------|--------|
| **Menu Browsing** | REQ-M-01 | Display all menu items | test_menu_page_returns_html | ✅ |
| | REQ-M-02 | Filter menu by category | test_menu_filter_by_category | ✅ |
| | REQ-M-03 | Show item availability | test_menu_unavailable_items_have_available_false | ✅ |
| **Cart Management** | REQ-C-01 | Add item to cart | test_cart_add_item | ✅ |
| | REQ-C-02 | Enforce quantity limits (max 20) | test_add_exceeds_max_quantity_raises_value_error | ✅ |
| | REQ-C-03 | Calculate correct total | test_cart_total_equals_unit_price_for_single_item | ✅ |
| **Order Placement** | REQ-O-01 | Place order with customer info | test_place_order | ✅ |
| | REQ-O-02 | Validate cart not empty | test_place_order_with_empty_items_returns_cart_empty_error | ✅ |
| | REQ-O-03 | Validate customer info | test_place_order_with_missing_customer_returns_missing_info_error | ✅ |
| **Order Tracking** | REQ-T-01 | Track order by ID | test_tracking_route_returns_success_for_valid_order | ✅ |
| | REQ-T-02 | Show status progress | test_valid_order_123_is_preparing | ✅ |
| | REQ-T-03 | Advance order status | test_advance_route_moves_order_to_next_status | ✅ |

### Coverage Summary
- **Total Requirements:** 12
- **Implemented:** 12
- **Test Coverage:** 100%
- **Orphaned Requirements:** 0

---

## 4. Persona Discovery & Edge Cases

### 4.1 Edge Case 1: Empty Cart Order Attempt
**Scenario:** Customer tries to place order with empty cart  
**AI Avatar:** "Forgot-to-eat" Pete - rushes through ordering  
**Requirement discovered:** System must prevent order submission with empty cart  
**Resolution:** Returns error "Cart is empty" with HTTP 400

### 4.2 Edge Case 2: Quantity Exceeds Maximum
**Scenario:** Customer enters quantity > 20  
**AI Avatar:** "Bulk-order" Brenda - wants to order for large group  
**Requirement discovered:** Enforce MAX_QUANTITY = 20 per item  
**Resolution:** Raises ValueError "Quantity must not exceed 20"

### 4.3 Edge Case 3: Missing Customer Information
**Scenario:** Customer submits checkout without name or address  
**AI Avatar:** "In-a-hurry" Hannah - wants fastest checkout  
**Requirement discovered:** Both name and address are required  
**Resolution:** Returns error "Missing customer info" with HTTP 400

### 4.4 Edge Case 4: Order Cancellation After Time Window
**Scenario:** Customer tries to cancel order after 2 minutes  
**AI Avatar:** "Changed-mind" Charlie - decides to cancel later  
**Requirement discovered:** Orders can only be cancelled within 2 minutes  
**Resolution:** Returns error "Cannot cancel confirmed order" after window

### 4.5 Edge Case 5: Invalid Order ID for Tracking
**Scenario:** Customer enters non-existent order ID  
**AI Avatar:** "Wrong-order" Wendy - mistyped her order number  
**Requirement discovered:** System must validate order existence  
**Resolution:** Returns 404 with error "Invalid order ID"

### 4.6 Edge Case 6: Maximum Cart Items Limit
**Scenario:** Customer tries to add 21st unique item  
**AI Avatar:** "Everything-taste" Eddie - wants to try everything  
**Requirement discovered:** Maximum 20 unique items in cart  
**Resolution:** Raises ValueError "CART_ITEM_LIMIT_REACHED: Cart is full (20 items max)"

### 4.7 Edge Case 7: Negative Quantity Rejection
**Scenario:** Customer enters negative number in quantity field  
**AI Avatar:** "Negative-nick" - testing system boundaries  
**Requirement discovered:** Quantity must be positive integer  
**Resolution:** Returns error "Quantity cannot be negative"

---

## 5. Requirements Traceability Justification

| Actor Type | Requirements Addressed | Rationale |
|------------|------------------------|-----------|
| Primary (Customer) | REQ-M-01, REQ-M-02, REQ-M-03, REQ-C-01, REQ-C-02, REQ-C-03, REQ-O-01, REQ-O-02, REQ-O-03, REQ-T-01, REQ-T-02, REQ-T-03 | All 12 requirements directly serve customer journey |
| Supporting (Kitchen/Delivery) | REQ-T-02, REQ-T-03 | Status updates support kitchen and delivery workflows |
| Offstage (Manager) | REQ-M-01, REQ-O-01 | Menu display and order placement for analytics |

---

## 6. Appendix: AI Prompts Used

1. **Prompt:** "Generate edge cases for a restaurant ordering system covering cart limits, order validation, and tracking scenarios"  
   **Used for:** Persona Discovery section

2. **Prompt:** "Create a traceability heatmap template for software requirements"  
   **Used for:** Traceability Matrix section

---

*Document Version: 1.0*  
*Date: [Current Date]*  
*Sub-system: Customer Ordering System*