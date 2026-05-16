from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from src import database
from src.auth import login_required, require_role
from src.order import get_all_orders

menu_bp = Blueprint('menu', __name__)


def _status_counts(orders):
    """Count orders by staff-facing status for the admin summary cards."""
    counts = {"pending": 0, "preparing": 0, "ready": 0, "delivered": 0}
    for order in orders:
        status = order.get("status")
        if status in counts:
            counts[status] += 1
    return counts


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


def update_menu_item(item_id, name, price, category, available):
    """Update an existing menu item.

    `available` is coerced to 0/1 via truthiness (so the caller can
    pass a Python bool, 0/1, or even a form-string).

    Returns {success: True} on success, or
    {success: False, error: "Item not found"} when item_id is unknown
    (UPDATE matched zero rows).
    """
    with database.get_db() as conn:
        cursor = conn.execute(
            "UPDATE menu_items "
            "SET name = ?, price = ?, category = ?, available = ? "
            "WHERE id = ?",
            (name, price, category, 1 if available else 0, item_id),
        )
        if cursor.rowcount == 0:
            return {"success": False, "error": "Item not found"}
        return {"success": True}


def delete_menu_item(item_id):
    """Hard-delete a menu item.

    Returns {success: True} on success, or
    {success: False, error: "Item not found"} when item_id is unknown
    (DELETE matched zero rows).

    NOTE: order_items rows may reference this menu_item_id. There is
    no FK cascade, so those rows keep the now-orphaned id. Historical
    order records remain intact via the embedded name/price snapshot
    in order_items. If you ever need referential integrity, swap to
    soft-delete (set available=0) instead.
    """
    with database.get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM menu_items WHERE id = ?",
            (item_id,),
        )
        if cursor.rowcount == 0:
            return {"success": False, "error": "Item not found"}
        return {"success": True}


@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({'items': []})


# --- Admin routes ---

@menu_bp.route('/admin', methods=['GET'])
@login_required
@require_role("admin")
def admin_view():
    return render_template(
        "admin.html",
        menu_items=get_all_menu_items(),
        status_counts=_status_counts(get_all_orders()),
    )


@menu_bp.route('/admin/menu/add', methods=['POST'])
@login_required
@require_role("admin")
def admin_menu_add():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip() or None
    try:
        price = float(request.form.get("price", "0"))
    except ValueError:
        flash("Invalid price", "error")
        return redirect(url_for("menu.admin_view"))

    result = add_menu_item(name, price, category)
    if not result["success"]:
        flash(result["error"], "error")
    return redirect(url_for("menu.admin_view"))


@menu_bp.route('/admin/menu/update', methods=['POST'])
@login_required
@require_role("admin")
def admin_menu_update():
    try:
        item_id = int(request.form.get("item_id", "0"))
        price = float(request.form.get("price", "0"))
    except ValueError:
        flash("Invalid item id or price", "error")
        return redirect(url_for("menu.admin_view"))

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip() or None
    available = bool(request.form.get("available"))  # checkbox: 'on' or absent

    result = update_menu_item(item_id, name, price, category, available)
    if not result["success"]:
        flash(result["error"], "error")
    return redirect(url_for("menu.admin_view"))


@menu_bp.route('/admin/menu/delete', methods=['POST'])
@login_required
@require_role("admin")
def admin_menu_delete():
    try:
        item_id = int(request.form.get("item_id", "0"))
    except ValueError:
        flash("Invalid item id", "error")
        return redirect(url_for("menu.admin_view"))

    result = delete_menu_item(item_id)
    if not result["success"]:
        flash(result["error"], "error")
    return redirect(url_for("menu.admin_view"))