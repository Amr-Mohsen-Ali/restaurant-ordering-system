from flask import Blueprint, jsonify

order_bp = Blueprint('order', __name__)


@order_bp.route('/place-order', methods=['POST'])
def place_order():
    return jsonify({'order_id': '', 'status': 'Preparing'}), 201