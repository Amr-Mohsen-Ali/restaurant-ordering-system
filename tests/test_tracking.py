import pytest

from src import create_app
from src.tracking import (
    get_order_details,
    get_order_status,
    is_empty_order_id,
    update_order_status,
)


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def test_valid_order_123_is_preparing():
    assert get_order_status("123") == "Preparing"


def test_valid_order_456_is_out_for_delivery():
    assert get_order_status("456") == "Out for Delivery"


def test_valid_order_789_is_delivered():
    assert get_order_status("789") == "Delivered"


def test_additional_order_321_is_preparing():
    assert get_order_status("321") == "Preparing"


def test_order_details_include_items_and_total():
    order = get_order_details("123")

    assert order["id"] == "123"
    assert order["items"] == ["Burger", "Fries"]
    assert order["total"] == 12.50
    assert order["status"] == "Preparing"


def test_invalid_order_id_raises_value_error():
    with pytest.raises(ValueError, match="Invalid order ID"):
        get_order_status("999")


def test_empty_order_id_is_detected():
    assert is_empty_order_id("") is True
    assert is_empty_order_id("   ") is True


def test_non_empty_order_id_is_detected():
    assert is_empty_order_id("123") is False


def test_tracking_route_returns_success_for_valid_order(client):
    response = client.get("/track/123")

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert data["status"] == "Preparing"
    assert data["order"]["id"] == "123"
    assert data["order"]["items"] == ["Burger", "Fries"]
    assert data["order"]["total"] == 12.50


def test_tracking_route_returns_error_for_invalid_order(client):
    response = client.get("/track/999")

    assert response.status_code == 404
    assert response.get_json() == {
        "success": False,
        "error": "Invalid order ID",
    }


def test_update_order_status_changes_status():
    updated_order = update_order_status("321", "Out for Delivery")

    assert updated_order["status"] == "Out for Delivery"

    update_order_status("321", "Preparing")


def test_update_order_status_rejects_invalid_status():
    with pytest.raises(ValueError, match="Invalid status"):
        update_order_status("123", "Cooking")


def test_advance_route_moves_order_to_next_status(client):
    update_order_status("321", "Preparing")

    response = client.post("/track/321/advance")

    assert response.status_code == 200
    assert response.get_json()["status"] == "Out for Delivery"

    update_order_status("321", "Preparing")