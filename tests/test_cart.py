import pytest
from src import create_app
from src.cart import Cart
from src.database import CartItem, db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_cart_table(app):
    with app.app_context():
        CartItem.query.delete()
        db.session.commit()


def test_cart_get(client):
    response = client.get('/cart')
    assert response.status_code == 200


def test_cart_add_item(client):
    response = client.post('/cart/add', json={'item_id': '1', 'price': 75.0, 'quantity': 1})
    assert response.status_code == 200, "Should return 200 on successful add"
    assert response.get_json()["success"] is True


def test_cart_add_item_persists_to_database(client, app):
    client.post('/cart/add', json={
        'item_id': '1',
        'item_name': 'Pizza',
        'price': 75.0,
        'quantity': 2,
    })

    with app.app_context():
        item = CartItem.query.filter_by(item_id='1').first()

    assert item is not None
    assert item.name == 'Pizza'
    assert item.quantity == 2


def test_cart_data_reads_database_items(client):
    client.post('/cart/add', json={
        'item_id': '1',
        'item_name': 'Pizza',
        'price': 75.0,
        'quantity': 2,
    })

    response = client.get('/cart/data')
    data = response.get_json()

    assert data["items"][0]["item_id"] == "1"
    assert data["items"][0]["quantity"] == 2
    assert data["total"] == 150.0


def test_checkout_clears_database_cart_after_order(client, app):
    client.post('/cart/add', json={
        'item_id': '1',
        'item_name': 'Pizza',
        'price': 75.0,
        'quantity': 1,
    })

    response = client.post('/checkout', data={
        'name': 'Gaber',
        'address': '123 Main St',
    })

    assert response.status_code == 302
    with app.app_context():
        assert CartItem.query.count() == 0


# tests/test_cart.py
# TDD Step 1 — these tests MUST fail before cart.py exists.
# Linked requirements: REQ-C-01, REQ-C-03 | Scenarios: SC-CART-01, SC-CART-02, SC-CART-03
#
# NOTE: The original doc test imported "from cart import Cart".
# In the application package, Cart now lives in src.cart and is imported above.


# ─────────────────────────────────────────────
#  Shared test data
# ─────────────────────────────────────────────

BURGER = {"item_id": "item_001", "name": "Classic Burger", "unit_price": 75.00}
FRIES  = {"item_id": "item_002", "name": "Fries",          "unit_price": 30.00}


# ─────────────────────────────────────────────
#  Fixture — fresh cart before every test
# ─────────────────────────────────────────────


@pytest.fixture
def empty_cart():
    """Returns a brand-new Cart instance for each test."""
    return Cart()


# ─────────────────────────────────────────────
#  SC-CART-01 — Happy path: add one item
# ─────────────────────────────────────────────

def test_add_single_item_returns_success(empty_cart):
    """add_to_cart returns success=True when a valid item is added."""
    result = empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert result["success"] is True


def test_add_single_item_appears_in_cart(empty_cart):
    """Item is present in cart items after add_to_cart."""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert BURGER["item_id"] in empty_cart.items


def test_add_single_item_cart_count_is_one(empty_cart):
    """cart_item_count == 1 after adding one item with quantity 1."""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert empty_cart.cart_item_count == 1


# ─────────────────────────────────────────────
#  SC-CART-01 + REQ-C-03 — Total calculation
# ─────────────────────────────────────────────

def test_cart_total_equals_unit_price_for_single_item(empty_cart):
    """cart_total == unit_price when quantity is 1. (REQ-C-03: tolerance ±0.01 EGP)"""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=1)

    assert abs(empty_cart.cart_total - 75.00) <= 0.01


# ─────────────────────────────────────────────
#  SC-CART-02 — Total recalculates for quantity > 1
# ─────────────────────────────────────────────

def test_cart_total_multiplies_by_quantity(empty_cart):
    """cart_total == unit_price × quantity for a single item type."""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=3)

    assert abs(empty_cart.cart_total - 225.00) <= 0.01  # 75.00 × 3


def test_cart_total_sums_multiple_items(empty_cart):
    """cart_total == sum of all (unit_price × quantity) lines. (REQ-C-03)"""
    empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=2)
    empty_cart.add_to_cart(FRIES["item_id"],  FRIES["unit_price"],  quantity=1)

    expected = (75.00 * 2) + (30.00 * 1)  # = 180.00
    assert abs(empty_cart.cart_total - expected) <= 0.01


# ─────────────────────────────────────────────
#  SC-CART-03 — Wrong path: invalid inputs
# ─────────────────────────────────────────────

def test_add_negative_quantity_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for quantity < 1. (SC-CART-03)"""
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=-1)


def test_add_zero_quantity_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for quantity == 0."""
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=0)


def test_add_exceeds_max_quantity_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for quantity > 20. (REQ-C-02)"""
    with pytest.raises(ValueError, match="Quantity must not exceed 20"):
        empty_cart.add_to_cart(BURGER["item_id"], BURGER["unit_price"], quantity=21)


def test_add_empty_item_id_raises_value_error(empty_cart):
    """add_to_cart raises ValueError for blank item_id."""
    with pytest.raises(ValueError, match="item_id must not be empty"):
        empty_cart.add_to_cart("", BURGER["unit_price"], quantity=1)
