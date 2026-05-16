ORDER_STATUS_PREPARING = "Preparing"
ORDER_STATUS_OUT_FOR_DELIVERY = "Out for Delivery"
ORDER_STATUS_DELIVERED = "Delivered"

ORDER_STATUSES = (
    ORDER_STATUS_PREPARING,
    ORDER_STATUS_OUT_FOR_DELIVERY,
    ORDER_STATUS_DELIVERED,
)

RESERVATION_STATUS_PENDING = "Pending"
RESERVATION_STATUS_CONFIRMED = "Confirmed"
RESERVATION_STATUS_SEATED = "Seated"
RESERVATION_STATUS_CANCELLED = "Cancelled"

RESERVATION_STATUSES = (
    RESERVATION_STATUS_PENDING,
    RESERVATION_STATUS_CONFIRMED,
    RESERVATION_STATUS_SEATED,
    RESERVATION_STATUS_CANCELLED,
)

ROLE_CUSTOMER = "customer"
ROLE_STAFF = "staff"
ROLE_ADMIN = "admin"

USER_ROLES = (
    ROLE_CUSTOMER,
    ROLE_STAFF,
    ROLE_ADMIN,
)

TIME_SLOTS = (
    "12:00",
    "14:00",
    "16:00",
    "18:00",
    "20:00",
    "22:00",
)

RESERVATION_DURATION_HOURS = 2

TABLES = (
    {"id": "T1", "number": "1", "label": "Window 1", "capacity": 2, "zone": "Window"},
    {"id": "T2", "number": "2", "label": "Window 2", "capacity": 2, "zone": "Window"},
    {"id": "T3", "number": "3", "label": "Garden 3", "capacity": 4, "zone": "Garden"},
    {"id": "T4", "number": "4", "label": "Garden 4", "capacity": 4, "zone": "Garden"},
    {"id": "T5", "number": "5", "label": "Family 5", "capacity": 6, "zone": "Family"},
    {"id": "T6", "number": "6", "label": "Family 6", "capacity": 8, "zone": "Family"},
)


def is_valid_order_status(status):
    return status in ORDER_STATUSES


def is_valid_reservation_status(status):
    return status in RESERVATION_STATUSES


def is_valid_role(role):
    return role in USER_ROLES


def get_table(table_number):
    normalized = str(table_number).strip()
    for table in TABLES:
        if table["number"] == normalized or table["id"] == normalized:
            return table
    return None
