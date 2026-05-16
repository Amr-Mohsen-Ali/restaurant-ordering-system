"""Authentication module.

register_user / login_user persist and verify accounts against the users
table (werkzeug.security for password hashing). get_current_user reads
the authenticated user from the Flask session; login_required and
require_role gate views behind session presence and role membership.
"""

from functools import wraps

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from src.constants import ROLE_CUSTOMER
from src.database import db, User

auth_bp = Blueprint('auth', __name__)


def register_user(username, password, role=ROLE_CUSTOMER):
    """Register a new user account.

    Hashes the password via werkzeug.security and inserts a row into
    the users table. Returns {success: True, user_id: int} on success,
    or {success: False, error: "Username already exists"} on duplicate.
    """
    password_hash = generate_password_hash(password)
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {"success": False, "error": "Username already exists"}
    
    new_user = User(username=username, password_hash=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    return {"success": True, "user_id": new_user.id}


def login_user(username, password):
    """Authenticate a user by username and password.

    Returns the same error message ('Invalid credentials') for both
    'username not found' and 'wrong password' to prevent username
    enumeration. Returns {success: True, user: {id, username, role}} on success,
    or {success: False, error: "Invalid credentials"} on any failure.
    """
    user = User.query.filter_by(username=username).first()

    if user is None:
        return {"success": False, "error": "Invalid credentials"}

    if not check_password_hash(user.password_hash, password):
        return {"success": False, "error": "Invalid credentials"}

    return {
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        },
    }


def get_current_user():
    """Return the authenticated user dict from the session, or None."""
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


# --- Routes ---

@auth_bp.route('/login', methods=['GET'])
def login_view():
    return render_template("login.html")


@auth_bp.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    result = login_user(username, password)
    if result["success"]:
        session["user"] = result["user"]
        return redirect("/menu")
    flash(result["error"], "error")
    return render_template("login.html", username=username), 400


@auth_bp.route('/register', methods=['GET'])
def register_view():
    return render_template("register.html")


@auth_bp.route('/register', methods=['POST'])
def register_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    result = register_user(username, password)
    if result["success"]:
        return redirect(url_for("auth.login_view"))
    flash(result["error"], "error")
    return render_template("register.html", username=username), 400


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop("user", None)
    return redirect("/login")
