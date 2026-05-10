from flask import Blueprint, jsonify, request, render_template

cart_bp = Blueprint('cart', __name__)

# This holds your cart data while the server runs
# (If your TDD Cart class is in another file, this mocks the connection for the UI)
current_cart = {
    "items": [],
    "total": 0.00
}

# 1. This loads your beautiful HTML page when someone visits the /cart URL
@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    return render_template('cart.html')

# 2. This is the exact route your cart.js file is looking for!
@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    item_id = data.get('item_id')
    price = float(data.get('price', 0))
    quantity = int(data.get('quantity', 1))

    # Reject negative numbers (Your TDD requirement!)
    if quantity < 1:
        return jsonify({"success": False, "error": "Quantity cannot be negative"})

    # Update the cart
    current_cart['items'].append({"item_id": item_id, "price": price, "quantity": quantity})
    current_cart['total'] += (price * quantity)

    # Send the success message and new total back to cart.js
    return jsonify({
        "success": True,
        "total": current_cart['total']
    })
