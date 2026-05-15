"""Unit tests for staff panel functions in src.order.

Covers DB-backed staff features: get_all_orders and update_order_status.
Each test uses the `db` fixture from conftest.py to operate against an
isolated SQLite database in a tempdir.
"""

from src.database import get_db
from src.order import get_all_orders


# --- get_all_orders ---

def test_get_all_orders_returns_list_after_insert(db):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO orders "
            "(id, customer_name, customer_address, status, total, placed_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("ORD-9001", "Test User", "123 Test St", "pending", 19.50, "2026-05-16T12:00:00"),
        )

    result = get_all_orders()

    assert len(result) > 0


# --- update_order_status ---

def test_update_order_status_with_valid_status_returns_success(db):
    from src.order import update_order_status

    with get_db() as conn:
        conn.execute(
            "INSERT INTO orders "
            "(id, customer_name, customer_address, status, total, placed_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("ORD-9002", "Test User", "123 Test St", "pending", 10.0, "2026-05-16T12:00:00"),
        )

    result = update_order_status("ORD-9002", "preparing")

    assert result["success"] is True


def test_update_order_status_with_invalid_status_returns_invalid_status_error(db):
    from src.order import update_order_status

    with get_db() as conn:
        conn.execute(
            "INSERT INTO orders "
            "(id, customer_name, customer_address, status, total, placed_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("ORD-9003", "Test User", "123 Test St", "pending", 10.0, "2026-05-16T12:00:00"),
        )

    result = update_order_status("ORD-9003", "bogus")

    assert result["error"] == "Invalid status"


def test_update_order_status_with_unknown_order_id_returns_not_found_error(db):
    from src.order import update_order_status

    result = update_order_status("ORD-NONEXISTENT", "preparing")

    assert result["error"] == "Order not found"
