"""Authentication module.

register_user persists new accounts to the users table with bcrypt-style
password hashing via werkzeug.security. The decorators (login_required,
require_role) and get_current_user are still stubs in this commit and
will be replaced with real session-backed implementations later.
"""

import sqlite3
from functools import wraps

from werkzeug.security import check_password_hash, generate_password_hash

from src import database


def register_user(username, password, role="customer"):
    """Register a new user account.

    Hashes the password via werkzeug.security and inserts a row into
    the users table. The UNIQUE constraint on username prevents
    duplicates at the DB level; we translate IntegrityError to a
    friendly error rather than doing a pre-check SELECT (the
    constraint-based approach is race-condition safe).

    Returns {success: True, user_id: int} on success, or
    {success: False, error: "Username already exists"} on duplicate.
    """
    password_hash = generate_password_hash(password)
    try:
        with database.get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, password_hash, role) "
                "VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            return {"success": True, "user_id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "Username already exists"}


def login_user(username, password):
    """Authenticate a user by username and password.

    Returns the same error message ('Invalid credentials') for both
    'username not found' and 'wrong password' to prevent username
    enumeration. The returned user dict deliberately excludes
    password_hash so it is safe to store in the session.

    Returns {success: True, user: {id, username, role}} on success, or
    {success: False, error: "Invalid credentials"} on any failure.
    """
    with database.get_db() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, role FROM users "
            "WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        return {"success": False, "error": "Invalid credentials"}

    if not check_password_hash(row["password_hash"], password):
        return {"success": False, "error": "Invalid credentials"}

    return {
        "success": True,
        "user": {
            "id": row["id"],
            "username": row["username"],
            "role": row["role"],
        },
    }


def get_current_user():
    """Return the currently-logged-in user.

    STUB: always returns the same staff user. Replace with session-based
    lookup when real auth is wired up.
    """
    return {"id": 1, "username": "staff1", "role": "staff"}


def login_required(view_func):
    """Decorator that gates a view behind authentication.

    STUB: currently allows every request through. Replace with a real
    session/identity check when auth lands.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)
    return wrapper


def require_role(*allowed_roles):
    """Decorator factory that gates a view behind a role check.

    STUB: currently allows every request through, regardless of the
    user's role. Kept so route definitions can declare role requirements
    today and have them enforced automatically when real auth lands.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
