"""Authentication module.

register_user / login_user persist and verify accounts against the users
table (werkzeug.security for password hashing). get_current_user reads
the authenticated user from the Flask session; login_required and
require_role gate views behind session presence and role membership.
"""

import sqlite3
from functools import wraps

from flask import abort, redirect, session
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
    """Return the authenticated user dict from the session, or None.

    The session is populated by the /login route handler after a
    successful login_user call. The dict has keys: id, username, role
    (no password_hash — it never enters the session).
    """
    return session.get("user")


def login_required(view_func):
    """Decorator that redirects to /login when the request is unauthenticated."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if get_current_user() is None:
            return redirect("/login")
        return view_func(*args, **kwargs)
    return wrapper


def require_role(*allowed_roles):
    """Decorator factory that aborts with 403 unless the user has one of `allowed_roles`."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user is None or user.get("role") not in allowed_roles:
                abort(403)
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
