from datetime import date, datetime

from src.constants import (
    RESERVATION_STATUS_CANCELLED,
    RESERVATION_STATUS_PENDING,
    TABLES,
    TIME_SLOTS,
    get_table,
    is_valid_reservation_status,
)
from src.database import Reservation, db


def parse_reservation_date(value):
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("Invalid reservation date")


def validate_slot(slot):
    if slot not in TIME_SLOTS:
        raise ValueError("Invalid reservation slot")
    return slot


def validate_party_size(party_size):
    try:
        size = int(party_size)
    except (TypeError, ValueError):
        raise ValueError("Party size must be a number")
    if size < 1:
        raise ValueError("Party size must be at least 1")
    return size


def validate_table_capacity(table_number, party_size):
    table = get_table(table_number)
    if table is None:
        raise ValueError("Invalid table")
    if party_size > table["capacity"]:
        raise ValueError("Party size exceeds table capacity")
    return table


def has_table_conflict(table_number, reservation_date, reservation_slot, exclude_id=None):
    query = Reservation.query.filter_by(
        table_number=str(table_number),
        reservation_date=reservation_date,
        reservation_slot=reservation_slot,
    ).filter(Reservation.status != RESERVATION_STATUS_CANCELLED)

    if exclude_id is not None:
        query = query.filter(Reservation.id != exclude_id)

    return query.first() is not None


def get_available_tables(reservation_date, reservation_slot, party_size):
    booking_date = parse_reservation_date(reservation_date)
    slot = validate_slot(reservation_slot)
    size = validate_party_size(party_size)

    available = []
    for table in TABLES:
        can_fit = size <= table["capacity"]
        is_booked = has_table_conflict(table["number"], booking_date, slot)
        available.append({
            **table,
            "available": can_fit and not is_booked,
            "booked": is_booked,
            "fits_party": can_fit,
        })
    return available


def create_reservation(data, user_id=None):
    customer_name = (data.get("customer_name") or data.get("name") or "").strip()
    contact = (data.get("contact") or "").strip()
    notes = (data.get("notes") or "").strip()
    table_number = str(data.get("table_number") or "").strip()
    booking_date = parse_reservation_date(data.get("reservation_date"))
    slot = validate_slot(data.get("reservation_slot"))
    party_size = validate_party_size(data.get("party_size"))

    if not customer_name:
        raise ValueError("Customer name is required")
    if not contact:
        raise ValueError("Contact info is required")

    table = validate_table_capacity(table_number, party_size)
    if has_table_conflict(table["number"], booking_date, slot):
        raise ValueError("Table is already booked for that date and slot")

    reservation = Reservation(
        user_id=user_id,
        customer_name=customer_name,
        contact=contact,
        party_size=party_size,
        reservation_date=booking_date,
        reservation_slot=slot,
        table_number=table["number"],
        status=RESERVATION_STATUS_PENDING,
        notes=notes,
    )
    db.session.add(reservation)
    db.session.commit()
    return reservation


def update_reservation_status(reservation_id, status):
    if not is_valid_reservation_status(status):
        raise ValueError("Invalid reservation status")

    reservation = Reservation.query.get(reservation_id)
    if reservation is None:
        raise ValueError("Reservation not found")

    reservation.status = status
    db.session.commit()
    return reservation


def can_view_reservation(user, reservation):
    if user is None:
        return False
    if user.get("role") in ("staff", "admin"):
        return True
    return reservation.user_id is not None and reservation.user_id == user.get("id")


def get_user_reservations(user_id):
    return Reservation.query.filter_by(user_id=user_id).order_by(
        Reservation.reservation_date.desc(),
        Reservation.reservation_slot.desc(),
    ).all()


def get_upcoming_reservations(limit=None):
    query = Reservation.query.order_by(
        Reservation.reservation_date.asc(),
        Reservation.reservation_slot.asc(),
    )
    if limit:
        query = query.limit(limit)
    return query.all()


def count_reservations_today():
    today = date.today()
    return Reservation.query.filter_by(reservation_date=today).filter(
        Reservation.status != RESERVATION_STATUS_CANCELLED
    ).count()
