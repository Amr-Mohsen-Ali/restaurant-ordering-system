# API Contracts

## Menu

### GET /menu
Renders the menu page (HTML).

### GET /api/menu
Returns all menu items. Supports optional `?category=` filter.

**Response (200)**
```json
{
  "items": [
    {"id": "1", "name": "Margherita Pizza", "price": 11.99, "category": "Main", "ingredients": ["Tomato", "Mozzarella", "Basil"], "available": true},
    {"id": "2", "name": "French Fries", "price": 3.99, "category": "Side", "ingredients": ["Potatoes", "Salt", "Oil"], "available": true}
  ]
}
```

**Query Parameters**

| Param | Type | Description |
|-------|------|-------------|
| category | string | Filter items by category (Main, Side, Dessert, Drink) |

## Cart

### GET /cart
Returns current cart contents.

**Response (200)**
```json
{
  "cart": {
    "items": [{"id": "1", "name": "Burger", "quantity": 2, "price": 9.99}],
    "total": 19.98
  }
}
```

### POST /cart
Add or remove items from cart.

**Request**
```json
{
  "itemId": "1",
  "action": "add" | "remove",
  "quantity": 1
}
```

**Response (200)**
```json
{
  "cart": {"items": [...], "total": 19.98}
}
```

## Order

### POST /place-order
Submit order from cart.

**Request**
```json
{
  "items": ["1", "2"],
  "total": 19.98
}
```

**Response (201)**
```json
{
  "order_id": "123",
  "status": "Preparing"
}
```

## Tracking

### GET /track/<order_id>
Get order status.

**Response (200)**
```json
{
  "success": true,
  "status": "Preparing" | "Out for Delivery" | "Delivered"
}
```

**Response (404)**
```json
{
  "success": false,
  "error": "Invalid order ID"
}
```