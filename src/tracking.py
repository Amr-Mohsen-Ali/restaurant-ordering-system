from flask import Blueprint, jsonify

tracking_bp = Blueprint('tracking', __name__)


@tracking_bp.route('/track/<order_id>', methods=['GET'])
def track_order(order_id):
    valid_orders = ['123', '456', '789']
    if order_id in valid_orders:
        return jsonify({'success': True, 'status': 'Preparing'}), 200
    return jsonify({'success': False, 'error': 'Invalid order ID'}), 404