from flask import Blueprint, jsonify

cart_bp = Blueprint('cart', __name__)


def add_to_cart(cart, item):
    """Append an item to the cart. Returns the updated cart.

    cart: list of cart-item dicts (each having id, name, price, quantity).
    item: dict to add.

    Minimal pure helper used by integration tests; full cart behaviour
    (quantity merging, removal, persistence) is owned by the cart feature.
    """
    cart.append(item)
    return cart


@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    return jsonify({'cart': {'items': [], 'total': 0}})


@cart_bp.route('/cart', methods=['POST'])
def update_cart():
    return jsonify({'cart': {'items': [], 'total': 0}})