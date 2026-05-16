from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for

from src import auth
from src.constants import TABLES, TIME_SLOTS
from src.database import Reservation
from src.reservations_service import (
    can_view_reservation,
    create_reservation,
    get_available_tables,
    get_user_reservations,
)

reservations_bp = Blueprint("reservations", __name__)


@reservations_bp.route("/reservations", methods=["GET"])
def reservations_page():
    user = auth.get_current_user()
    my_reservations = get_user_reservations(user["id"]) if user else []
    return render_template(
        "reservations.html",
        tables=TABLES,
        time_slots=TIME_SLOTS,
        my_reservations=my_reservations,
    )


@reservations_bp.route("/reservations", methods=["POST"])
@auth.login_required
def reservations_submit():
    user = auth.get_current_user()
    try:
        reservation = create_reservation(request.form, user_id=user["id"] if user else None)
    except ValueError as error:
        return render_template(
            "reservations.html",
            tables=TABLES,
            time_slots=TIME_SLOTS,
            error=str(error),
            form_data=request.form,
            my_reservations=get_user_reservations(user["id"]) if user else [],
        ), 400

    return redirect(url_for("reservations.reservation_detail", reservation_id=reservation.id))


@reservations_bp.route("/reservations/<int:reservation_id>", methods=["GET"])
@auth.login_required
def reservation_detail(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if not can_view_reservation(auth.get_current_user(), reservation):
        abort(403)
    return render_template("reservation_detail.html", reservation=reservation)


@reservations_bp.route("/api/reservations/availability", methods=["GET"])
def availability_api():
    try:
        tables = get_available_tables(
            request.args.get("date"),
            request.args.get("slot"),
            request.args.get("party_size", 1),
        )
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400
    return jsonify({"success": True, "tables": tables})
