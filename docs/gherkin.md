# Gherkin Scenarios

## Menu Browsing (Abdallah)

```gherkin
Feature: Menu Browsing
  As a customer
  I want to view the menu
  So that I can choose items to order

  Scenario: View all menu items
    Given I am on the menu page
    When I load the page
    Then I should see all available items

  Scenario: Filter by category
    Given I am on the menu page
    When I select "Main" category
    Then I should see only main dishes
```

## Cart (Hala)

```gherkin
Feature: Cart Management
  As a customer
  I want to manage my cart
  So that I can add or remove items before ordering

  Scenario: Add item to cart
    Given I am on the menu page
    When I click "Add" on an item
    Then the item should appear in my cart

  Scenario: Remove item from cart
    Given I have items in my cart
    When I click "Remove" on an item
    Then the item should be removed from my cart

  Scenario: View cart total
    Given I have items in my cart
    When I view my cart
    Then I should see the correct total
```

## Order Placement (Gaber)

```gherkin
Feature: Order Placement
  As a customer
  I want to place an order
  So that I can receive my food

  Scenario: Place order successfully
    Given I have items in my cart
    When I submit my order
    Then I should receive an order ID
    And the order status should be "Preparing"
```

## Order Tracking (Amr)

```gherkin
Feature: Order Tracking
  As a customer
  I want to track my order
  So that I know when it will arrive

  Scenario: Track valid order
    Given I have a valid order ID
    When I enter the order ID to track
    Then I should see the current status

  Scenario: Track invalid order
    Given I enter an invalid order ID
    When I try to track
    Then I should see an error message
```