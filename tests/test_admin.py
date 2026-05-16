"""Unit tests for admin menu functions in src.menu.

Each test uses the `db` fixture from conftest.py for an isolated
SQLite database (the menu_items table is created by init_db).
"""

from src.database import get_db
from src.menu import get_all_menu_items


# --- get_all_menu_items ---

def test_get_all_menu_items_returns_list_after_insert(db):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO menu_items (name, price, category, available) "
            "VALUES (?, ?, ?, ?)",
            ("Burger", 9.99, "Main", 1),
        )

    result = get_all_menu_items()

    assert len(result) > 0


# --- add_menu_item ---

def test_add_menu_item_with_valid_data_returns_success_true(db):
    from src.menu import add_menu_item

    result = add_menu_item("Pizza", 12.50, "Main")

    assert result["success"] is True


def test_add_menu_item_with_missing_name_returns_name_required_error(db):
    from src.menu import add_menu_item

    result = add_menu_item("", 12.50, "Main")

    assert result["error"] == "Name is required"
