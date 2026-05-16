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
