# D6 - Final Presentation Slide Deck
## Restaurant Ordering System - Customer Ordering Sub-system

---

## Slide 1: Title Slide

# Restaurant Ordering System
## Customer Ordering Sub-system

**Presented by:** [Group Name]  
**Date:** [Presentation Date]

---

## Slide 2: Project Overview

### What We Built
- Online food ordering system
- Browse menu by category
- Add items to shopping cart
- Place orders with delivery tracking

### Technology Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** pytest, Playwright
- **Deployment:** PythonAnywhere

---

## Slide 3: System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Menu      │────▶│    Cart     │────▶│  Checkout   │
│  (Browse)   │     │  (Manage)   │     │   (Order)   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Tracking   │
                                        │  (Follow)   │
                                        └─────────────┘
```

---

## Slide 4: Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Menu Browsing** | Filter by category, show availability | ✅ Complete |
| **Cart Management** | Add/remove items, quantity limits | ✅ Complete |
| **Order Placement** | Validate info, generate order ID | ✅ Complete |
| **Order Tracking** | Status progress, advance status | ✅ Complete |

---

## Slide 5: Requirements (D2 Highlights)

### Actor Classification
- **Primary:** Customer, Guest User
- **Supporting:** Kitchen Staff, Delivery Driver
- **Offstage:** Restaurant Manager

### Edge Cases Covered
1. Empty cart order attempt
2. Quantity exceeds maximum (20)
3. Missing customer information
4. Order cancellation after 2 minutes
5. Invalid order ID for tracking

---

## Slide 6: Design Specification (D3 Highlights)

### Gherkin Example
```gherkin
Scenario: Add item to cart
  Given I am on the menu page
  When I select quantity 2 of "Cheeseburger"
  And I click "Add to Cart"
  Then the item should be added to my cart
```

### API Contracts
- `/menu` - GET
- `/cart/add` - POST
- `/checkout` - POST
- `/track/<id>` - GET

---

## Slide 7: Testing (D4 Highlights)

### Test Results
- **Total Tests:** 90
- **Passed:** 90 ✅
- **Coverage:** 100%

### Test Pyramid
- 70% Unit Tests (63 tests)
- 20% Integration Tests (18 tests)
- 10% E2E Tests (9 tests)

---

## Slide 8: Implementation (D5)

### TDP Approach
1. Write failing test first
2. Implement feature
3. Verify test passes
4. Refactor if needed

### Vertical Slice
- UI Layer ✅
- Logic Layer ✅
- Data Layer ✅

---

## Slide 9: Demo

### Demo Video Link
[Insert ≤ 5 minute demo video]

### Shows:
1. Browse menu
2. Filter by category
3. Add to cart
4. Place order
5. Track order

---

## Slide 10: Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Connect features end-to-end | Updated templates to use shared data |
| Different order ID formats | Standardized to numeric IDs |
| Cart not showing in checkout | Created `/cart/data` API endpoint |
| Status mismatch with tracking | Changed "confirmed" to "Preparing" |

---

## Slide 11: Future Enhancements

### Potential Improvements
- Add real database (SQLite/PostgreSQL)
- User authentication system
- Payment integration
- Mobile app
- Kitchen display system

---

## Slide 12: Conclusion

### Summary
- ✅ Full ordering system implemented
- ✅ 100% test coverage
- ✅ All requirements traced
- ✅ API contracts defined

### Thank You!
**GitHub:** https://github.com/Amr-Mohsen-Ali/restaurant-ordering-system

---

## Appendix: AI Prompts Used

1. **Prompt:** "Generate edge cases for restaurant ordering system"
   - Used for: Persona Discovery (D2)

2. **Prompt:** "Create Gherkin scenarios for shopping cart"
   - Used for: BDD Scripts (D3)

3. **Prompt:** "Write pytest tests for Flask blueprint"
   - Used for: TDP Implementation (D5)

---

*Presentation Version: 1.0*  
*Date: [Current Date]*