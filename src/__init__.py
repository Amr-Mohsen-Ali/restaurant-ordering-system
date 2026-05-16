import os
from flask import Flask, render_template
from src.database import db, ensure_cart_columns, seed_orders, seed_users
from src import auth


def create_app(test_config=None):
    app = Flask(__name__, 
                template_folder="../templates",
                static_folder="../static")
    app.secret_key = 'dev-secret-key'

    if test_config and test_config.get('SQLALCHEMY_DATABASE_URI') == 'sqlite:///:memory:':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'restaurant.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        ensure_cart_columns()
        if not app.config.get('TESTING'):
            seed_orders()
            seed_users()

    @app.context_processor
    def inject_current_user():
        return {"current_user": auth.get_current_user()}

    @app.route('/')
    def home():
        return render_template('home.html')

    from src import menu, cart, order, tracking, reservations, kitchen
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(menu.menu_bp)
    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(tracking.tracking_bp)
    app.register_blueprint(reservations.reservations_bp)
    app.register_blueprint(kitchen.kitchen_bp)

    return app
