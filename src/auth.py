"""Authentication stub.

TEMPORARY — to be replaced when the real auth module ships.

- get_current_user() always returns a hardcoded staff user.
- login_required is a no-op decorator that always allows access.
- require_role(...) is a no-op decorator factory (kept for forward
  compatibility with the route signatures that will eventually use it).
"""

from functools import wraps


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
