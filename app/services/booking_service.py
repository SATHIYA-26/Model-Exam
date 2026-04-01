from __future__ import annotations

from typing import Any

from data.repository import Booking, Event, Repository


class BookingService:
    def __init__(self, repo: Repository | None = None) -> None:
        self.repo = repo or Repository.get_instance()

    def search_events(self, keyword: str | None = None) -> list[Event]:
        return self.repo.search_events(keyword)

    def book_event(self, username: str, event_id: int, seats: int) -> dict[str, Any]:
        if seats <= 0:
            raise ValueError("Seats must be positive")

        booking = self.repo.create_booking(username, event_id, seats)
        return {
            "id": booking.id,
            "username": username,
            "event_id": booking.event_id,
            "seats": booking.seats,
        }

    def cancel_booking(self, booking_id: int) -> None:
        booking = self.repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        self.repo.cancel_booking(booking_id)

    def get_bookings_for_user(self, username: str) -> list[Booking]:
        return self.repo.get_bookings_for_user(username)
