import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(20), primary_key=True)
    items = db.Column(db.JSON, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Preparing')
    customer_name = db.Column(db.String(100))
    customer_address = db.Column(db.String(200))
    estimated_time = db.Column(db.Integer, default=25)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'items': self.items,
            'total': self.total,
            'status': self.status,
            'estimated_time': self.estimated_time
        }


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }


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


def seed_orders():
    """Seed sample orders for testing. Call after db.create_all() within app_context."""
    if Order.query.first() is None:
        sample_orders = [
            Order(id='123', items=[{'name': 'Burger', 'price': 9.99, 'quantity': 2}], total=19.98, status='Preparing', customer_name='Ahmed', customer_address='123 Main St', estimated_time=15),
            Order(id='456', items=[{'name': 'Pizza', 'price': 12.99, 'quantity': 1}], total=12.99, status='Ready', customer_name='Sara', customer_address='456 Oak Ave', estimated_time=5),
            Order(id='789', items=[{'name': 'Salad', 'price': 7.50, 'quantity': 1}], total=7.50, status='Delivered', customer_name='Omar', customer_address='789 Pine Rd', estimated_time=0),
            Order(id='321', items=[{'name': 'Pasta', 'price': 11.00, 'quantity': 2}], total=22.00, status='Preparing', customer_name='Lina', customer_address='321 Elm St', estimated_time=20),
            Order(id='654', items=[{'name': 'Soda', 'price': 2.50, 'quantity': 3}], total=7.50, status='Ready', customer_name='Tariq', customer_address='654 Maple Dr', estimated_time=3),
            Order(id='987', items=[{'name': 'Burger', 'price': 9.99, 'quantity': 1}, {'name': 'Fries', 'price': 4.50, 'quantity': 1}], total=14.49, status='Preparing', customer_name='Nadia', customer_address='987 Cedar Ln', estimated_time=18),
        ]
        for order in sample_orders:
            db.session.add(order)
        db.session.commit()
        print("Seeded 6 sample orders to database.")