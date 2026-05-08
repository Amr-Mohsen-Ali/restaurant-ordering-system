from flask import Blueprint, jsonify

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    pass