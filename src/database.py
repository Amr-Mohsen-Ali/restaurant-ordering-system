import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from src.constants import (
    ORDER_STATUS_DELIVERED,
    ORDER_STATUS_OUT_FOR_DELIVERY,
    ORDER_STATUS_PREPARING,
    RESERVATION_STATUS_PENDING,
    ROLE_ADMIN,
    ROLE_STAFF,
)

db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(20), primary_key=True)
    order_items = db.Column(db.JSON, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default=ORDER_STATUS_PREPARING)
    customer_name = db.Column(db.String(100))
    customer_address = db.Column(db.String(200))
    estimated_time = db.Column(db.Integer, default=25)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'items': self.order_items,
            'total': self.total,
            'status': self.status,
            'estimated_time': self.estimated_time
        }


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(50))
    session_key = db.Column(db.String(80), index=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id or str(self.id),
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }


def ensure_cart_columns():
    """Add cart persistence columns when an existing SQLite DB predates them."""
    engine_name = db.engine.url.get_backend_name()
    if engine_name != "sqlite":
        return

    with db.engine.connect() as connection:
        columns = {
            row[1]
            for row in connection.exec_driver_sql("PRAGMA table_info(cart_items)").fetchall()
        }
        if "item_id" not in columns:
            connection.exec_driver_sql("ALTER TABLE cart_items ADD COLUMN item_id VARCHAR(50)")
        if "session_key" not in columns:
            connection.exec_driver_sql("ALTER TABLE cart_items ADD COLUMN session_key VARCHAR(80)")
        connection.commit()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    customer_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_slot = db.Column(db.String(10), nullable=False)
    table_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), default=RESERVATION_STATUS_PENDING)
    notes = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'customer_name': self.customer_name,
            'contact': self.contact,
            'party_size': self.party_size,
            'reservation_date': self.reservation_date.isoformat() if self.reservation_date else None,
            'reservation_slot': self.reservation_slot,
            'table_number': self.table_number,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


def seed_orders():
    """Seed sample orders for testing. Call after db.create_all() within app_context."""
    Order.query.filter_by(status='Ready').update({"status": ORDER_STATUS_OUT_FOR_DELIVERY})
    db.session.commit()

    if Order.query.first() is None:
        sample_orders = [
            Order(id='123', order_items=[{'name': 'Burger', 'price': 9.99, 'quantity': 2}], total=19.98, status=ORDER_STATUS_PREPARING, customer_name='Ahmed', customer_address='123 Main St', estimated_time=15),
            Order(id='456', order_items=[{'name': 'Pizza', 'price': 12.99, 'quantity': 1}], total=12.99, status=ORDER_STATUS_OUT_FOR_DELIVERY, customer_name='Sara', customer_address='456 Oak Ave', estimated_time=5),
            Order(id='789', order_items=[{'name': 'Salad', 'price': 7.50, 'quantity': 1}], total=7.50, status=ORDER_STATUS_DELIVERED, customer_name='Omar', customer_address='789 Pine Rd', estimated_time=0),
            Order(id='321', order_items=[{'name': 'Pasta', 'price': 11.00, 'quantity': 2}], total=22.00, status=ORDER_STATUS_PREPARING, customer_name='Lina', customer_address='321 Elm St', estimated_time=20),
            Order(id='654', order_items=[{'name': 'Soda', 'price': 2.50, 'quantity': 3}], total=7.50, status=ORDER_STATUS_OUT_FOR_DELIVERY, customer_name='Tariq', customer_address='654 Maple Dr', estimated_time=3),
            Order(id='987', order_items=[{'name': 'Burger', 'price': 9.99, 'quantity': 1}, {'name': 'Fries', 'price': 4.50, 'quantity': 1}], total=14.49, status=ORDER_STATUS_PREPARING, customer_name='Nadia', customer_address='987 Cedar Ln', estimated_time=18),
        ]
        for order in sample_orders:
            db.session.add(order)
        db.session.commit()
        print("Seeded 6 sample orders to database.")


def seed_users():
    """Seed admin and staff users for testing. Call after db.create_all() within app_context."""
    from werkzeug.security import generate_password_hash
    
    if User.query.filter_by(username='admin').first() is None:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role=ROLE_ADMIN
        )
        db.session.add(admin)
    
    if User.query.filter_by(username='staff').first() is None:
        staff = User(
            username='staff',
            password_hash=generate_password_hash('staff123'),
            role=ROLE_STAFF
        )
        db.session.add(staff)
    
    db.session.commit()
    print("Seeded admin and staff users.")
