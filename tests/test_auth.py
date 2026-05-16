"""Unit tests for auth functions in src.auth.

Each test uses the `db` fixture from conftest.py to operate against an
isolated SQLite database (with the users table pre-created by init_db).
"""


# --- register_user ---

def test_register_user_with_valid_data_returns_success_true(db):
    from src.auth import register_user

    result = register_user("alice", "securepass123")

    assert result["success"] is True


def test_register_user_with_duplicate_username_returns_username_exists_error(db):
    from src.auth import register_user

    register_user("bob", "firstpass")  # seed: first registration succeeds
    result = register_user("bob", "secondpass")  # same username again

    assert result["error"] == "Username already exists"


# --- login_user ---

def test_login_user_with_correct_password_returns_success_true(db):
    from src.auth import login_user, register_user

    register_user("charlie", "rightpass")

    result = login_user("charlie", "rightpass")

    assert result["success"] is True


def test_login_user_with_wrong_password_returns_invalid_credentials_error(db):
    from src.auth import login_user, register_user

    register_user("dana", "correctpass")

    result = login_user("dana", "wrongpass")

    assert result["error"] == "Invalid credentials"


def test_login_user_with_unknown_username_returns_invalid_credentials_error(db):
    from src.auth import login_user

    result = login_user("nonexistent", "anypass")

    assert result["error"] == "Invalid credentials"
