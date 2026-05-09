Feature: Cart management

  Scenario: Customer adds a menu item to the cart
    Given the customer is on the menu page
    And   the cart is currently empty
    When  the customer clicks "Add to Cart" on "Classic Burger"
    Then  "Classic Burger" appears in the cart
    And   the cart item count badge shows 1
    And   the cart total equals the price of "Classic Burger"

  Scenario: Customer increases the quantity of a cart item
    Given the customer has 1 "Classic Burger" in the cart
    When  the customer changes the quantity of "Classic Burger" to 3
    Then  the quantity of "Classic Burger" shows 3
    And   the cart total equals 3 × the price of "Classic Burger"
    And   the cart item count badge updates to 3

  Scenario: Customer enters a negative quantity
    Given the customer has 1 "Classic Burger" in the cart
    When  the customer sets the quantity of "Classic Burger" to -1
    Then  an error message "Quantity must be at least 1" is shown
    And   the quantity of "Classic Burger" remains 1
    And   the cart total is unchanged

  Scenario: Customer removes the only item, leaving the cart empty
    Given the customer has 1 "Classic Burger" in the cart
    When  the customer clicks the remove button on "Classic Burger"
    Then  the cart is empty
    And   an "Your cart is empty" message is displayed
    And   the cart total shows EGP 0.00
    And   the cart item count badge is hidden

  Scenario: Customer sets quantity to 0 which removes the item
    Given the customer has 2 "Fries" in the cart
    When  the customer sets the quantity of "Fries" to 0
    Then  a confirmation prompt "Remove Fries from cart?" appears
    And   if the customer confirms, "Fries" is removed from the cart
    And   the cart total updates to EGP 0.00
