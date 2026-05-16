from datetime import date

import pytest

from src.constants import (
    ORDER_STATUS_PREPARING,
    RESERVATION_STATUS_CONFIRMED,
    RESERVATION_STATUS_PENDING,
    is_valid_order_status,
    is_valid_reservation_status,
)
from src.database import Reservation
from src.reservations_service import create_reservation, get_available_tables, update_reservation_status


def login_as(client, role="admin", user_id=1, username=None):
    with client.session_transaction() as session:
        session["user"] = {
            "id": user_id,
            "username": username or role,
            "role": role,
        }


def test_status_validation_helpers():
    assert is_valid_order_status(ORDER_STATUS_PREPARING) is True
    assert is_valid_order_status("Ready") is False
    assert is_valid_reservation_status(RESERVATION_STATUS_PENDING) is True
    assert is_valid_reservation_status("Preparing") is False


def test_admin_dashboard_requires_admin(client, app_context):
    login_as(client, role="staff")

    response = client.get("/admin/dashboard")

    assert response.status_code == 403


def test_admin_dashboard_renders_for_admin(client, app_context):
    login_as(client, role="admin")

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert b"Restaurant Dashboard" in response.data
    assert b"Reservations Today" in response.data


def test_staff_page_includes_reservation_management(client, app_context):
    login_as(client, role="staff")

    response = client.get("/staff")

    assert response.status_code == 200
    assert b"Staff Operations" in response.data
    assert b"Reservations" in response.data


def test_create_reservation_with_nullable_user_id(app_context):
    reservation = create_reservation({
        "customer_name": "Mona",
        "contact": "mona@example.com",
        "party_size": "2",
        "reservation_date": "2026-06-01",
        "reservation_slot": "18:00",
        "table_number": "1",
    })

    assert reservation.id is not None
    assert reservation.user_id is None
    assert reservation.status == RESERVATION_STATUS_PENDING
    assert reservation.reservation_date == date(2026, 6, 1)
    assert reservation.reservation_slot == "18:00"


def test_duplicate_reservation_rejected(app_context):
    payload = {
        "customer_name": "Mona",
        "contact": "mona@example.com",
        "party_size": "2",
        "reservation_date": "2026-06-02",
        "reservation_slot": "18:00",
        "table_number": "1",
    }
    create_reservation(payload)

    with pytest.raises(ValueError, match="already booked"):
        create_reservation(payload)


def test_capacity_validation_rejects_large_party(app_context):
    with pytest.raises(ValueError, match="capacity"):
        create_reservation({
            "customer_name": "Large Group",
            "contact": "group@example.com",
            "party_size": "8",
            "reservation_date": "2026-06-03",
            "reservation_slot": "18:00",
            "table_number": "1",
        })


def test_availability_marks_booked_table_unavailable(app_context):
    create_reservation({
        "customer_name": "Mona",
        "contact": "mona@example.com",
        "party_size": "2",
        "reservation_date": "2026-06-04",
        "reservation_slot": "18:00",
        "table_number": "1",
    })

    tables = get_available_tables("2026-06-04", "18:00", 2)
    booked = next(table for table in tables if table["number"] == "1")

    assert booked["available"] is False
    assert booked["booked"] is True


def test_reservation_status_update(app_context):
    reservation = create_reservation({
        "customer_name": "Mona",
        "contact": "mona@example.com",
        "party_size": "2",
        "reservation_date": "2026-06-05",
        "reservation_slot": "18:00",
        "table_number": "1",
    })

    updated = update_reservation_status(reservation.id, RESERVATION_STATUS_CONFIRMED)

    assert updated.status == RESERVATION_STATUS_CONFIRMED


def test_reservation_post_requires_login(client, app_context):
    response = client.post("/reservations", data={
        "customer_name": "Mona",
        "contact": "mona@example.com",
        "party_size": "2",
        "reservation_date": "2026-06-06",
        "reservation_slot": "18:00",
        "table_number": "1",
    })

    assert response.status_code == 302
    assert response.headers["Location"] == "/login"


def test_logged_in_customer_can_create_and_view_own_reservation(client, app_context):
    login_as(client, role="customer", user_id=42, username="mona")

    response = client.post("/reservations", data={
        "customer_name": "Mona",
        "contact": "mona@example.com",
        "party_size": "2",
        "reservation_date": "2026-06-07",
        "reservation_slot": "18:00",
        "table_number": "1",
    })

    assert response.status_code == 302
    reservation = Reservation.query.filter_by(customer_name="Mona").first()
    detail = client.get(f"/reservations/{reservation.id}")
    assert detail.status_code == 200
    assert b"Your table is requested" in detail.data
