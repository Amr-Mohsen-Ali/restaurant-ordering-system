from flask import Blueprint, jsonify, request, render_template

cart_bp = Blueprint('cart', __name__)

current_cart = {
    "items": [],
    "total": 0.00
}


def get_cart():
    """Return current cart data."""
    return current_cart

# cart.py
# Linked requirements: REQ-C-01, REQ-C-02, REQ-C-03
# Linked scenarios:    SC-CART-01, SC-CART-02, SC-CART-03


class Cart:
    """Manages the customer's shopping cart for the ordering system."""

    MAX_QUANTITY = 20   # REQ-C-02: single item quantity ceiling
    MAX_ITEMS    = 20   # REQ-C-02: unique item count ceiling

    def __init__(self):
        """
        self.items  — dict  { item_id: {"quantity": int, "unit_price": float} }
        """
        self.items: dict = {}

    # ── read-only properties ───────────────────────────────────────

    @property
    def cart_item_count(self) -> int:
        """Total number of individual units across all items."""
        return sum(v["quantity"] for v in self.items.values())

    @property
    def cart_total(self) -> float:
        """
        Sum of (unit_price × quantity) for every item.
        Rounded to 2 decimal places — satisfies REQ-C-03 tolerance ±0.01 EGP.
        """
        total = sum(
            v["unit_price"] * v["quantity"]
            for v in self.items.values()
        )
        return round(total, 2)

    # ── core methods ───────────────────────────────────────────────

    def add_to_cart(self, item_id: str, unit_price: float, quantity: int) -> dict:
        """
        Add an item to the cart or increase its quantity if already present.

        Args:
            item_id    (str):   unique identifier for the menu item
            unit_price (float): price per single unit in EGP
            quantity   (int):   number of units to add (1–20)

        Returns:
            dict: { "success": True, "cart_item_count": int, "cart_total": float }

        Raises:
            ValueError: if item_id is blank, quantity < 1, or quantity > 20
        """
        # ── input validation (order matches test assertions) ───────────
        if not item_id or not item_id.strip():
            raise ValueError("item_id must not be empty")

        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        if quantity > self.MAX_QUANTITY:
            raise ValueError("Quantity must not exceed 20")

        # ── cart item limit check (REQ-C-02) ───────────────────────────
        if item_id not in self.items and len(self.items) >= self.MAX_ITEMS:
            raise ValueError("CART_ITEM_LIMIT_REACHED: Cart is full (20 items max)")

        # ── update or insert ───────────────────────────────────────────
        if item_id in self.items:
            self.items[item_id]["quantity"] += quantity
        else:
            self.items[item_id] = {
                "quantity":   quantity,
                "unit_price": unit_price,
            }

        return {
            "success":         True,
            "cart_item_count": self.cart_item_count,
            "cart_total":      self.cart_total,
        }


def add_to_cart(cart, item):
    """Append an item to the cart. Returns the updated cart.

    cart: list of cart-item dicts (each having id, name, price, quantity).
    item: dict to add.

    Minimal pure helper used by integration tests; full cart behaviour
    (quantity merging, removal, persistence) is owned by the cart feature.
    """
    cart.append(item)
    return cart


# 1. This loads your beautiful HTML page when someone visits the /cart URL
@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    return render_template('cart.html')

# 2. This is the exact route your cart.js file is looking for!
@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart_route():
    data = request.json
    item_id = data.get('item_id')
    item_name = data.get('item_name', item_id)
    price = float(data.get('price', 0))
    quantity = int(data.get('quantity', 1))

    if quantity < 1:
        return jsonify({"success": False, "error": "Quantity cannot be negative"})

    found = False
    for item in current_cart['items']:
        if item['item_id'] == item_id:
            item['quantity'] += quantity
            found = True
            break
            
    if not found:
        current_cart['items'].append({"item_id": item_id, "name": item_name, "price": price, "quantity": quantity})
        
    current_cart['total'] += (price * quantity)

    # Send the success message and new total back to cart.js
    return jsonify({
        "success": True,
        "total": current_cart['total']
    })


@cart_bp.route('/cart/update', methods=['POST'])
def update_cart_item():
    data = request.json
    item_id = data.get('item_id')
    action = data.get('action') # 'increase', 'decrease', 'remove'

    for item in current_cart['items']:
        if item['item_id'] == item_id:
            if action == 'increase':
                item['quantity'] += 1
                current_cart['total'] += item['price']
            elif action == 'decrease':
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                    current_cart['total'] -= item['price']
                else:
                    current_cart['total'] -= (item['price'] * item['quantity'])
                    current_cart['items'].remove(item)
            elif action == 'remove':
                current_cart['total'] -= (item['price'] * item['quantity'])
                current_cart['items'].remove(item)
            break

    # Avoid floating point precision issues and negative totals
    current_cart['total'] = round(max(0, current_cart['total']), 2)

    return jsonify({"success": True, "total": current_cart['total']})


@cart_bp.route('/cart/data', methods=['GET'])
def get_cart_data():
    """Return current cart data for checkout page."""
    return jsonify(current_cart)
