from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev-secret-key'

    from src import menu, cart, order, tracking
    app.register_blueprint(menu.menu_bp)
    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(tracking.tracking_bp)

    return app