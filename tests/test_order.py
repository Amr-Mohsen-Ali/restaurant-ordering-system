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


def test_place_order(client):
    response = client.post('/place-order', json={'items': ['1'], 'total': 9.99})
    assert response.status_code == 201, "Should return 201 Created"
    data = response.get_json()
    assert 'order_id' in data, "Response should contain 'order_id'"
    assert 'status' in data, "Response should contain 'status'"