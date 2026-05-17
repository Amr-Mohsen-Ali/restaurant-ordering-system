from flask import Blueprint, jsonify, render_template, request
from src.database import MenuItem

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/menu', methods=['GET'])
def menu_page():
    items = MenuItem.query.all()
    menu_list = [item.to_dict() for item in items]
    categories = sorted(set(item['category'] for item in menu_list))
    return render_template('menu.html', items=menu_list, categories=categories)


@menu_bp.route('/api/menu', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    query = MenuItem.query
    if category:
        query = query.filter_by(category=category)
    items = query.all()
    return jsonify({'items': [item.to_dict() for item in items]})
