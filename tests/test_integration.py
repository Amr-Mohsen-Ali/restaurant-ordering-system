import pytest

from src import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def test_tracking_page_loads(client):
    response = client.get("/tracking")

    assert response.status_code == 200
    assert b"Order Tracking" in response.data


def test_api_returns_status_for_valid_order(client):
    response = client.get("/track/123")

    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "status": "Preparing",
    }


def test_api_returns_invalid_order_for_unknown_id(client):
    response = client.get("/track/999")

    assert response.status_code == 404
    assert response.get_json() == {
        "success": False,
        "error": "Invalid order ID",
    }


def test_api_handles_empty_order_id(client):
    response = client.get("/track/%20")

    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "error": "Order ID is required",
    }