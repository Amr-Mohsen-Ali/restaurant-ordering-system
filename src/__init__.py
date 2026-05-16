from flask import Flask


def create_app():
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static")
    app.secret_key = 'dev-secret-key'

    from src import auth, menu, cart, order, tracking
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(menu.menu_bp)
    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(order.order_bp)
    app.register_blueprint(tracking.tracking_bp)

    # Make the current user available to every rendered template,
    # so base.html can swap nav links based on auth state.
    @app.context_processor
    def inject_current_user():
        return {"current_user": auth.get_current_user()}

    return app