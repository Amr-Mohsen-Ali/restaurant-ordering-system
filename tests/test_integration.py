import pytest


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.skip(reason="depends on Amr's tracking feature")
def test_full_order_flow(client, app_context):
    menu_response = client.get('/menu')
    assert menu_response.status_code == 200, "Menu should be accessible"


def test_tracking_page_loads(client, app_context):
    response = client.get("/tracking")

    assert response.status_code == 200
    assert b"Track Your" in response.data

    order_response = client.post('/place-order', json={
        'items': [{'name': 'Burger', 'price': 9.99, 'quantity': 1}],
        'total': 9.99,
        'customer': {'name': 'Gaber', 'address': '123 Main St'},
    })
    assert order_response.status_code == 201, "Order should be created"



def test_api_returns_status_for_valid_order(client, app_context):
    response = client.get("/track/123")

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert data["status"] == "Preparing"
    assert data["order"]["id"] == "123"
    assert data["order"]["total"] == 12.50


def test_api_returns_invalid_order_for_unknown_id(client, app_context):
    response = client.get("/track/999")

    assert response.status_code == 404
    assert response.get_json() == {
        "success": False,
        "error": "Invalid order ID",
    }


def test_api_handles_empty_order_id(client, app_context):
    response = client.get("/track/%20")

    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "error": "Order ID is required",
    }


def test_api_handles_special_characters_as_invalid_id(client, app_context):
    response = client.get("/track/%21%40%23")

    assert response.status_code == 404
    assert response.get_json() == {
        "success": False,
        "error": "Invalid order ID",
    }


def test_api_can_advance_order_status(client, app_context):
    client.post("/track/321/status", json={"status": "Preparing"})

    response = client.post("/track/321/advance")

    assert response.status_code == 200
    assert response.get_json()["status"] == "Out for Delivery"

    client.post("/track/321/status", json={"status": "Preparing"})


def test_api_rejects_invalid_status_update(client, app_context):
    response = client.post("/track/123/status", json={"status": "Cooking"})

    assert response.status_code == 400
    assert response.get_json() == {
        "success": False,
        "error": "Invalid status",
    }