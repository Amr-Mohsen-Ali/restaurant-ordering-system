import pytest
from src import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_track_valid_order(client):
    pass


def test_track_invalid_order(client):
    pass