from flask import Blueprint, jsonify

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    return jsonify({'cart': {'items': [], 'total': 0}})


@cart_bp.route('/cart', methods=['POST'])
def update_cart():
    return jsonify({'cart': {'items': [], 'total': 0}})