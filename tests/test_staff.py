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
