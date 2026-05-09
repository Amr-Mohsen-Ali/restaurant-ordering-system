import datetime
from unittest.mock import patch

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


@pytest.fixture
def valid_request():
    return {
        "items": ["1"],
        "total": 9.99,
        "customer": {"name": "Gaber", "address": "123 Main St"},
    }


def test_place_order(client):
    response = client.post('/place-order', json={
        'items': ['1'],
        'total': 9.99,
        'customer': {'name': 'Gaber', 'address': '123 Main St'},
    })
    assert response.status_code == 201, "Should return 201 Created"
    data = response.get_json()
    assert 'order_id' in data, "Response should contain 'order_id'"
    assert 'status' in data, "Response should contain 'status'"


# =============================================================================
# POST /place-order — extended response shape
# =============================================================================

def test_place_order_response_success_is_true(client, valid_request):
    response = client.post('/place-order', json=valid_request)
    assert response.get_json()["success"] is True


def test_place_order_response_status_is_confirmed(client, valid_request):
    response = client.post('/place-order', json=valid_request)
    assert response.get_json()["status"] == "confirmed"


def test_place_order_response_estimated_time_is_25(client, valid_request):
    response = client.post('/place-order', json=valid_request)
    assert response.get_json()["estimated_time"] == 25


def test_place_order_response_order_id_has_ord_prefix(client, valid_request):
    response = client.post('/place-order', json=valid_request)
    assert response.get_json()["order_id"].startswith("ORD-")


# --- POST /place-order — error cases ---

def test_place_order_with_empty_items_returns_400(client):
    response = client.post('/place-order', json={
        "items": [],
        "total": 0,
        "customer": {"name": "Gaber", "address": "123 Main St"},
    })
    assert response.status_code == 400


def test_place_order_with_empty_items_returns_cart_empty_error(client):
    response = client.post('/place-order', json={
        "items": [],
        "total": 0,
        "customer": {"name": "Gaber", "address": "123 Main St"},
    })
    assert response.get_json()["error"] == "Cart is empty"


def test_place_order_with_missing_customer_returns_400(client):
    response = client.post('/place-order', json={"items": ["1"], "total": 9.99})
    assert response.status_code == 400


def test_place_order_with_missing_customer_returns_missing_info_error(client):
    response = client.post('/place-order', json={"items": ["1"], "total": 9.99})
    assert response.get_json()["error"] == "Missing customer info"


# =============================================================================
# GET /confirmation/<order_id>
# =============================================================================

def test_confirmation_happy_path_returns_matching_order_id(client, valid_request):
    placed = client.post('/place-order', json=valid_request).get_json()
    response = client.get(f'/confirmation/{placed["order_id"]}')
    assert response.get_json()["order_id"] == placed["order_id"]


def test_confirmation_happy_path_returns_status_confirmed(client, valid_request):
    placed = client.post('/place-order', json=valid_request).get_json()
    response = client.get(f'/confirmation/{placed["order_id"]}')
    assert response.get_json()["status"] == "confirmed"


def test_confirmation_happy_path_returns_estimated_time(client, valid_request):
    placed = client.post('/place-order', json=valid_request).get_json()
    response = client.get(f'/confirmation/{placed["order_id"]}')
    assert response.get_json()["estimated_time"] == 25


def test_confirmation_with_unknown_id_returns_not_found_error(client):
    response = client.get('/confirmation/ORD-99999999')
    assert response.get_json()["error"] == "Order not found"


# =============================================================================
# POST /cancel-order/<order_id>
# =============================================================================

def test_cancel_order_happy_path_returns_success_true(client, valid_request):
    placed = client.post('/place-order', json=valid_request).get_json()
    response = client.post(f'/cancel-order/{placed["order_id"]}')
    assert response.get_json()["success"] is True


def test_cancel_order_happy_path_returns_cancelled_message(client, valid_request):
    placed = client.post('/place-order', json=valid_request).get_json()
    response = client.post(f'/cancel-order/{placed["order_id"]}')
    assert response.get_json()["message"] == "Order cancelled"


def test_cancel_order_with_unknown_id_returns_not_found_error(client):
    response = client.post('/cancel-order/ORD-99999999')
    assert response.get_json()["error"] == "Order not found"


# --- Cancel after 2-minute window ---

ROUTE_BASE_TIME = datetime.datetime(2026, 5, 9, 12, 0, 0)


def test_cancel_order_after_window_returns_400(client, valid_request):
    with patch("src.order._now", return_value=ROUTE_BASE_TIME):
        placed = client.post('/place-order', json=valid_request).get_json()
    future = ROUTE_BASE_TIME + datetime.timedelta(minutes=2, seconds=1)
    with patch("src.order._now", return_value=future):
        response = client.post(f'/cancel-order/{placed["order_id"]}')
    assert response.status_code == 400


def test_cancel_order_after_window_returns_cannot_cancel_error(client, valid_request):
    with patch("src.order._now", return_value=ROUTE_BASE_TIME):
        placed = client.post('/place-order', json=valid_request).get_json()
    future = ROUTE_BASE_TIME + datetime.timedelta(minutes=2, seconds=1)
    with patch("src.order._now", return_value=future):
        response = client.post(f'/cancel-order/{placed["order_id"]}')
    assert response.get_json()["error"] == "Cannot cancel confirmed order"