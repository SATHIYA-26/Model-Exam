from flask import Flask, jsonify, redirect, render_template, request, session, url_for, flash

from services.auth_service import AuthService
from services.booking_service import BookingService


app = Flask(__name__)
app.secret_key = "change-me-in-production"

auth_service = AuthService()
booking_service = BookingService()


@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Username and password required", "error")
            return render_template("login.html")
        if auth_service.authenticate(username, password):
            session["username"] = username
            flash("Login successful", "success")
            return redirect(url_for("events_page"))
        flash("Invalid credentials", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect(url_for("login_page"))


def _require_login():
    if "username" not in session:
        flash("Please log in first", "error")
        return False
    return True


@app.route("/events", methods=["GET", "POST"])
def events_page():
    if not _require_login():
        return redirect(url_for("login_page"))

    if request.method == "POST":
        event_id = int(request.form.get("event_id"))
        seats = int(request.form.get("seats", 1))
        try:
            booking_service.book_event(session["username"], event_id, seats)
            flash("Booking successful", "success")
        except ValueError as ex:
            flash(str(ex), "error")

    keyword = request.args.get("q")
    events = booking_service.search_events(keyword=keyword or None)
    return render_template("events.html", events=events)


@app.route("/book/<int:event_id>", methods=["POST"])
def book_event_page(event_id: int):
    if not _require_login():
        return redirect(url_for("login_page"))
    seats = int(request.form.get("seats", 1))
    try:
        booking_service.book_event(session["username"], event_id, seats)
        flash("Booking successful", "success")
    except ValueError as ex:
        flash(str(ex), "error")
    return redirect(url_for("events_page"))


@app.route("/bookings", methods=["GET"])
def bookings_page():
    if not _require_login():
        return redirect(url_for("login_page"))
    bookings = booking_service.get_bookings_for_user(session["username"])
    return render_template("bookings.html", bookings=bookings)


@app.route("/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking_page(booking_id: int):
    if not _require_login():
        return redirect(url_for("login_page"))
    try:
        booking_service.cancel_booking(booking_id)
        flash("Booking cancelled", "success")
    except ValueError as ex:
        flash(str(ex), "error")
    return redirect(url_for("bookings_page"))


# Existing JSON API endpoints (optional, kept for reference)
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if auth_service.authenticate(username, password):
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/events", methods=["GET"])
def api_list_events():
    keyword = request.args.get("q")
    events = booking_service.search_events(keyword=keyword)
    return jsonify([
        {"id": e.id, "name": e.name, "available_seats": e.available_seats}
        for e in events
    ])


@app.route("/api/book", methods=["POST"])
def api_book_event():
    data = request.get_json() or {}
    username = data.get("username")
    event_id = data.get("event_id")
    seats = int(data.get("seats", 1))

    try:
        booking = booking_service.book_event(username, event_id, seats)
        return jsonify(booking), 201
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400


@app.route("/api/cancel", methods=["POST"])
def api_cancel_booking():
    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    try:
        booking_service.cancel_booking(booking_id)
        return jsonify({"message": "Booking cancelled"})
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400


if __name__ == "__main__":
    app.run(debug=True)
