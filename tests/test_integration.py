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
    data = response.get_json()

    assert data["success"] is True
    assert data["status"] == "Preparing"
    assert data["order"] == {
        "id": "123",
        "items": ["Burger", "Fries"],
        "total": 12.50,
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


def test_api_handles_special_characters_as_invalid_id(client):
    response = client.get("/track/%21%40%23")

    assert response.status_code == 404
    assert response.get_json() == {
        "success": False,
        "error": "Invalid order ID",
    }


def test_api_can_advance_order_status(client):
    client.post("/track/321/status", json={"status": "Preparing"})

    response = client.post("/track/321/advance")

    assert response.status_code == 200
    assert response.get_json()["status"] == "Out for Delivery"

    client.post("/track/321/status", json={"status": "Preparing"})


def test_api_rejects_invalid_status_update(client):
    response = client.post("/track/123/status", json={"status": "Cooking"})

    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "error": "Invalid status",
    }