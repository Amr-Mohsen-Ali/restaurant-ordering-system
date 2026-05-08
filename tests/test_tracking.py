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
    response = client.get('/track/123')
    assert response.status_code == 200, "Should return 200 for valid order"
    data = response.get_json()
    assert data.get('success') is True, "Should return success: true"
    assert 'status' in data, "Response should contain 'status'"


def test_track_invalid_order(client):
    response = client.get('/track/invalid-id')
    assert response.status_code == 404, "Should return 404 for invalid order"
    data = response.get_json()
    assert data.get('success') is False, "Should return success: false"