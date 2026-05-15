"""SQLite storage for staff-facing order data.

Customer-facing order state remains in src.order's in-memory dicts
(_orders, _placed_at) so the existing customer-facing tests stay green.
This module persists the staff-facing fulfillment lifecycle: pending →
preparing → ready → delivered. Staff status is independent of the
customer-facing 'confirmed' status.

Schema (denormalised — no users table; auth is stubbed):
    orders(id, customer_name, customer_address, status, total, placed_at)
    order_items(id, order_id, menu_item_id, name, quantity, price)
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    status TEXT NOT NULL,
    total REAL NOT NULL,
    placed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    menu_item_id TEXT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
"""


_db_path = None


def init_db(path):
    """Set the active database path and create tables if missing.

    Idempotent: safe to call multiple times against the same path.
    """
    global _db_path
    _db_path = Path(path)
    _db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(_db_path) as conn:
        conn.executescript(SCHEMA)


def is_initialized():
    return _db_path is not None


@contextmanager
def get_db():
    """Yield a sqlite3 connection with Row factory enabled.

    Raises RuntimeError if init_db() has not been called.
    """
    if _db_path is None:
        raise RuntimeError(
            "Database has not been initialised. Call init_db(path) first."
        )
    conn = sqlite3.connect(_db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
