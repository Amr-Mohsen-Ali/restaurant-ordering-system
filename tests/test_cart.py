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


def test_cart_get(client):
    response = client.get('/cart')
    data = response.get_json()
    assert 'cart' in data, "Response should contain 'cart' key"


def test_cart_add_item(client):
    response = client.post('/cart', json={'itemId': '1', 'action': 'add', 'quantity': 1})
    assert response.status_code == 200, "Should return 200 on successful add"