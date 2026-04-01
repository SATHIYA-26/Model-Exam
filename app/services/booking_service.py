from __future__ import annotations

from typing import Any

from app.data.repository import InMemoryRepository


class BookingService:
    def __init__(self, repo: InMemoryRepository | None = None) -> None:
        self.repo = repo or InMemoryRepository.get_instance()

    def search_events(self, keyword: str | None = None) -> list[dict[str, Any]]:
        return self.repo.search_events(keyword)

    def book_event(self, username: str, event_id: int, seats: int) -> dict[str, Any]:
        if seats <= 0:
            raise ValueError("Seats must be positive")

        user = self.repo.get_user_by_username(username)
        if not user:
            raise ValueError("User not found")

        event = self.repo.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        if event["available_seats"] < seats:
            raise ValueError("No seats available")

        booking = self.repo.create_booking(username, event_id, seats)
        return booking

    def cancel_booking(self, booking_id: int) -> None:
        booking = self.repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        self.repo.cancel_booking(booking_id)
