# API Contracts

## Menu

### GET /menu
Returns all menu items.

**Response (200)**
```json
{
  "items": [
    {"id": "1", "name": "Burger", "price": 9.99, "category": "Main"},
    {"id": "2", "name": "Fries", "price": 3.99, "category": "Side"}
  ]
}
```

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
Submit order from cart. Requires customer information.

**Request**
```json
{
  "items": ["1", "2"],
  "total": 19.98,
  "customer": {
    "name": "Jane Doe",
    "address": "123 Main St"
  }
}
```

**Response (201)**
```json
{
  "success": true,
  "order_id": "ORD-1042",
  "status": "confirmed",
  "estimated_time": 25
}
```

**Response (400)** — empty cart or missing customer info
```json
{
  "success": false,
  "error": "Cart is empty"
}
```
or
```json
{
  "success": false,
  "error": "Missing customer info"
}
```

### GET /confirmation/<order_id>
Retrieve full details for a placed order.

**Response (200)**
```json
{
  "order_id": "ORD-1042",
  "items": [
    {"id": "1", "name": "Burger", "price": 9.99, "quantity": 1}
  ],
  "total": 9.99,
  "estimated_time": 25,
  "status": "confirmed"
}
```

**Response (404)**
```json
{
  "success": false,
  "error": "Order not found"
}
```

### POST /cancel-order/<order_id>
Cancel an order. Only permitted within 2 minutes of placement.

**Response (200)**
```json
{
  "success": true,
  "message": "Order cancelled"
}
```

**Response (400)** — order is older than the 2-minute cancellation window
```json
{
  "success": false,
  "error": "Cannot cancel confirmed order"
}
```

**Response (404)** — order_id does not exist
```json
{
  "success": false,
  "error": "Order not found"
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