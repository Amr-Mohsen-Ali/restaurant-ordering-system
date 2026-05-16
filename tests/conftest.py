import pytest
from src import create_app
from src.database import db, Order, CartItem


def seed_test_orders():
    Order.query.delete()
    orders = [
        Order(id='123', order_items=['Burger', 'Fries'], total=12.50, status='Preparing', customer_name='Ahmed', customer_address='123 Main St', estimated_time=15),
        Order(id='456', order_items=['Pizza'], total=12.99, status='Out for Delivery', customer_name='Sara', customer_address='456 Oak Ave', estimated_time=5),
        Order(id='789', order_items=['Salad'], total=7.50, status='Delivered', customer_name='Omar', customer_address='789 Pine Rd', estimated_time=0),
        Order(id='321', order_items=['Pasta'], total=11.00, status='Preparing', customer_name='Lina', customer_address='321 Elm St', estimated_time=20),
    ]
    for order in orders:
        db.session.add(order)
    db.session.commit()


@pytest.fixture(autouse=True)
def app():
    print("\n[CONFTEST] Creating app with in-memory DB")
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        db.create_all()
        seed_test_orders()
        print("[CONFTEST] App ready, seed_test_orders called")
        yield app
    print("[CONFTEST] Teardown")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def reset_cart(app):
    with app.app_context():
        CartItem.query.delete()
        db.session.commit()
        yield
        CartItem.query.delete()
        db.session.commit()


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield