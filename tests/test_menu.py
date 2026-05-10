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


def test_menu_page_returns_html(client):
    response = client.get('/menu')
    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_menu_api_returns_items(client):
    response = client.get('/api/menu')
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) > 0


def test_menu_items_have_required_fields(client):
    response = client.get('/api/menu')
    data = response.get_json()
    for item in data['items']:
        assert 'id' in item
        assert 'name' in item
        assert 'price' in item
        assert 'category' in item
        assert 'ingredients' in item
        assert 'available' in item


def test_menu_filter_by_category(client):
    response = client.get('/api/menu?category=Main')
    data = response.get_json()
    assert all(item['category'] == 'Main' for item in data['items'])


def test_menu_filter_by_category_dessert(client):
    response = client.get('/api/menu?category=Dessert')
    data = response.get_json()
    assert all(item['category'] == 'Dessert' for item in data['items'])


def test_menu_includes_unavailable_items(client):
    response = client.get('/api/menu')
    data = response.get_json()
    unavailable = [item for item in data['items'] if not item['available']]
    assert len(unavailable) > 0


def test_menu_unavailable_items_have_available_false(client):
    response = client.get('/api/menu?category=Main')
    data = response.get_json()
    for item in data['items']:
        if item['name'] == 'Caesar Salad':
            assert item['available'] is False


def test_menu_filter_category_with_no_matches(client):
    response = client.get('/api/menu?category=NonExistent')
    data = response.get_json()
    assert len(data['items']) == 0
