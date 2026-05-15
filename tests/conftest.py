"""Shared pytest fixtures for the test suite.

The `db` fixture initialises a fresh SQLite database in a temp directory
for tests that exercise staff-side persistence. Each test that requests
it gets an isolated database that is discarded automatically.
"""

import pytest

from src import database


@pytest.fixture
def db(tmp_path):
    """Initialise a fresh SQLite database for this test."""
    db_path = tmp_path / "test.db"
    database.init_db(db_path)
    yield db_path
    # Reset module-level state so subsequent tests don't see this DB.
    database._db_path = None
