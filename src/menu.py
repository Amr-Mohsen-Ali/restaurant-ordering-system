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


def add_menu_item(name, price, category):
    """Insert a new menu item.

    Validates that name is non-empty (stripping whitespace) before
    writing. The `available` column defaults to 1 in the schema, so
    new items are visible to customers by default.

    Returns {success: True, item_id: int} on success, or
    {success: False, error: "Name is required"} when name is empty.
    """
    if not name or not name.strip():
        return {"success": False, "error": "Name is required"}

    with database.get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO menu_items (name, price, category) "
            "VALUES (?, ?, ?)",
            (name.strip(), price, category),
        )
        return {"success": True, "item_id": cursor.lastrowid}


@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({'items': []})