"""Fake order data used by order tracking.

The team project does not use a database for this feature, so this file keeps
the sample order IDs and statuses in one shared place.
"""

ORDERS = {
    "123": {
        "id": "123",
        "items": ["Burger", "Fries"],
        "total": 12.50,
        "status": "Preparing",
    },
    "456": {
        "id": "456",
        "items": ["Pizza"],
        "total": 15.00,
        "status": "Out for Delivery",
    },
    "789": {
        "id": "789",
        "items": ["Pasta", "Salad"],
        "total": 18.75,
        "status": "Delivered",
    },
    "321": {
        "id": "321",
        "items": ["Chicken Wrap", "Lemonade"],
        "total": 11.25,
        "status": "Preparing",
    },
    "ABC-1": {
        "id": "ABC-1",
        "items": ["Soup"],
        "total": 6.00,
        "status": "Out for Delivery",
    },
    "000": {
        "id": "000",
        "items": [],
        "total": 0.00,
        "status": "Preparing",
    },
}