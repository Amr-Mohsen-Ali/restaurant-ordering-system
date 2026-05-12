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


@pytest.mark.skip(reason="depends on Amr's tracking feature")
def test_full_order_flow(client):
    menu_response = client.get('/menu')
    assert menu_response.status_code == 200, "Menu should be accessible"

    cart_response = client.get('/cart')
    assert cart_response.status_code == 200, "Cart should be accessible"

    order_response = client.post('/place-order', json={
        'items': ['1'],
        'total': 9.99,
        'customer': {'name': 'Gaber', 'address': '123 Main St'},
    })
    assert order_response.status_code == 201, "Order should be created"

    data = order_response.get_json()
    order_id = data.get('order_id')

    track_response = client.get(f'/track/{order_id}')
    assert track_response.status_code == 200, "Should be able to track order"