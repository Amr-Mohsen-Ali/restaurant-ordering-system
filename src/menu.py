from flask import Blueprint, jsonify

from src import database

menu_bp = Blueprint('menu', __name__)


def get_all_menu_items():
    """Return all menu items, ordered by category then name.

    Each item dict has: id, name, price, category, available.
    Returns [] when the menu_items table is empty.
    """
    with database.get_db() as conn:
        rows = conn.execute(
            "SELECT id, name, price, category, available "
            "FROM menu_items ORDER BY category, name"
        ).fetchall()
        return [dict(row) for row in rows]


@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({'items': []})