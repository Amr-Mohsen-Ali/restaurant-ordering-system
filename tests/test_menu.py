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


def test_menu_returns_items(client):
    response = client.get('/menu')
    data = response.get_json()
    assert 'items' in data, "Response should contain 'items' key"