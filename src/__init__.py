from flask import Flask, render_template


def create_app():
    app = Flask(__name__, 
                template_folder="../templates",
                static_folder="../static")
    app.secret_key = 'dev-secret-key'

    @app.route('/')
    def home():
        return render_template('home.html')

    from src import menu, cart, order, tracking
    app.register_blueprint(menu.menu_bp)
    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(tracking.tracking_bp)

    return app