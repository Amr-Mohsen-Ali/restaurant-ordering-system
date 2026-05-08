from flask import Blueprint, jsonify

tracking_bp = Blueprint('tracking', __name__)


@tracking_bp.route('/track/<order_id>', methods=['GET'])
def track_order(order_id):
    pass