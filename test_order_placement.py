import pytest

from order_placement import get_confirmation, place_order


@pytest.fixture
def valid_cart():
    return [{"id": 1, "name": "Burger", "price": 10.00, "quantity": 1}]


@pytest.fixture
def valid_customer():
    return {"name": "Gaber", "address": "123 Main St"}


# --- Happy path ---

def test_place_order_returns_success_true(valid_cart, valid_customer):
    result = place_order(valid_cart, valid_customer)
    assert result["success"] is True


def test_place_order_returns_order_id_with_ord_prefix(valid_cart, valid_customer):
    result = place_order(valid_cart, valid_customer)
    assert result["order_id"].startswith("ORD-")


def test_place_order_returns_estimated_time_of_25(valid_cart, valid_customer):
    result = place_order(valid_cart, valid_customer)
    assert result["estimated_time"] == 25


# --- Empty cart ---

def test_place_order_with_empty_cart_returns_success_false(valid_customer):
    result = place_order([], valid_customer)
    assert result["success"] is False


def test_place_order_with_empty_cart_returns_cart_empty_error(valid_customer):
    result = place_order([], valid_customer)
    assert result["error"] == "Cart is empty"


# --- None / missing inputs ---

def test_place_order_with_none_cart_returns_success_false(valid_customer):
    result = place_order(None, valid_customer)
    assert result["success"] is False


def test_place_order_with_none_customer_returns_success_false(valid_cart):
    result = place_order(valid_cart, None)
    assert result["success"] is False


# --- Missing name ---

def test_place_order_missing_name_returns_success_false(valid_cart):
    customer = {"address": "123 Main St"}
    result = place_order(valid_cart, customer)
    assert result["success"] is False


def test_place_order_missing_name_returns_missing_info_error(valid_cart):
    customer = {"address": "123 Main St"}
    result = place_order(valid_cart, customer)
    assert result["error"] == "Missing customer info"


# --- Missing address ---

def test_place_order_missing_address_returns_success_false(valid_cart):
    customer = {"name": "Gaber"}
    result = place_order(valid_cart, customer)
    assert result["success"] is False


def test_place_order_missing_address_returns_missing_info_error(valid_cart):
    customer = {"name": "Gaber"}
    result = place_order(valid_cart, customer)
    assert result["error"] == "Missing customer info"


# --- Boundary: empty strings count as missing ---

def test_place_order_with_empty_name_string_returns_success_false(valid_cart):
    customer = {"name": "", "address": "123 Main St"}
    result = place_order(valid_cart, customer)
    assert result["success"] is False


def test_place_order_with_empty_address_string_returns_success_false(valid_cart):
    customer = {"name": "Gaber", "address": ""}
    result = place_order(valid_cart, customer)
    assert result["success"] is False


# =============================================================================
# get_confirmation
# =============================================================================

@pytest.fixture
def placed_order(valid_cart, valid_customer):
    return place_order(valid_cart, valid_customer)


# --- Happy path ---

def test_get_confirmation_returns_matching_order_id(placed_order):
    result = get_confirmation(placed_order["order_id"])
    assert result["order_id"] == placed_order["order_id"]


def test_get_confirmation_returns_items_from_placed_cart(valid_cart, valid_customer):
    placed = place_order(valid_cart, valid_customer)
    result = get_confirmation(placed["order_id"])
    assert result["items"] == valid_cart


def test_get_confirmation_returns_correct_total_for_multi_item_cart(valid_customer):
    cart = [
        {"id": 1, "name": "Burger", "price": 10.00, "quantity": 2},
        {"id": 2, "name": "Fries", "price": 4.50, "quantity": 1},
    ]
    placed = place_order(cart, valid_customer)
    result = get_confirmation(placed["order_id"])
    assert result["total"] == 24.50


def test_get_confirmation_returns_estimated_time(placed_order):
    result = get_confirmation(placed_order["order_id"])
    assert result["estimated_time"] == 25


def test_get_confirmation_returns_status_confirmed(placed_order):
    result = get_confirmation(placed_order["order_id"])
    assert result["status"] == "confirmed"


# --- Not found ---

def test_get_confirmation_with_unknown_id_returns_success_false():
    result = get_confirmation("ORD-99999999")
    assert result["success"] is False


def test_get_confirmation_with_unknown_id_returns_not_found_error():
    result = get_confirmation("ORD-99999999")
    assert result["error"] == "Order not found"


# --- None / empty input ---

def test_get_confirmation_with_none_id_returns_success_false():
    result = get_confirmation(None)
    assert result["success"] is False


def test_get_confirmation_with_empty_string_id_returns_success_false():
    result = get_confirmation("")
    assert result["success"] is False
