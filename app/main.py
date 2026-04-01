from flask import Flask, request, jsonify

from app.services.auth_service import AuthService
from app.services.booking_service import BookingService

app = Flask(__name__)

auth_service = AuthService()
booking_service = BookingService()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if auth_service.authenticate(username, password):
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/events", methods=["GET"])
def list_events():
    keyword = request.args.get("q")
    events = booking_service.search_events(keyword=keyword)
    return jsonify(events)


@app.route("/book", methods=["POST"])
def book_event():
    data = request.get_json() or {}
    username = data.get("username")
    event_id = data.get("event_id")
    seats = int(data.get("seats", 1))

    try:
        booking = booking_service.book_event(username, event_id, seats)
        return jsonify(booking), 201
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400


@app.route("/cancel", methods=["POST"])
def cancel_booking():
    data = request.get_json() or {}
    booking_id = data.get("booking_id")
    try:
        booking_service.cancel_booking(booking_id)
        return jsonify({"message": "Booking cancelled"})
    except ValueError as ex:
        return jsonify({"error": str(ex)}), 400


if __name__ == "__main__":
    app.run(debug=True)
