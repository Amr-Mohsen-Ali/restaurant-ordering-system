from flask import Blueprint, jsonify

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    pass


@cart_bp.route('/cart', methods=['POST'])
def update_cart():
    pass