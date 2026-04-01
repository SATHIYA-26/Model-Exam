from __future__ import annotations

from typing import Any, ClassVar


class InMemoryRepository:
    _instance: ClassVar["InMemoryRepository" | None] = None

    def __init__(self) -> None:
        # Simple in‑memory structures for demo only
        self.users: list[dict[str, Any]] = [
            {"id": 1, "username": "student1", "password": "password"},
            {"id": 2, "username": "admin", "password": "admin"},
        ]
        self.events: list[dict[str, Any]] = [
            {"id": 1, "name": "Tech Talk", "available_seats": 50},
            {"id": 2, "name": "Workshop", "available_seats": 30},
        ]
        self.bookings: list[dict[str, Any]] = []
        self._next_booking_id = 1

    @classmethod
    def get_instance(cls) -> "InMemoryRepository":
        if cls._instance is None:
            cls._instance = InMemoryRepository()
        return cls._instance

    # User operations
    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        return next((u for u in self.users if u["username"] == username), None)

    # Event operations
    def search_events(self, keyword: str | None = None) -> list[dict[str, Any]]:
        if not keyword:
            return list(self.events)
        kw = keyword.lower()
        return [e for e in self.events if kw in e["name"].lower()]

    def get_event_by_id(self, event_id: int) -> dict[str, Any] | None:
        return next((e for e in self.events if e["id"] == event_id), None)

    # Booking operations
    def create_booking(self, username: str, event_id: int, seats: int) -> dict[str, Any]:
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        event["available_seats"] -= seats
        booking = {
            "id": self._next_booking_id,
            "username": username,
            "event_id": event_id,
            "seats": seats,
        }
        self._next_booking_id += 1
        self.bookings.append(booking)
        return booking

    def get_booking_by_id(self, booking_id: int) -> dict[str, Any] | None:
        return next((b for b in self.bookings if b["id"] == booking_id), None)

    def cancel_booking(self, booking_id: int) -> None:
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        event = self.get_event_by_id(booking["event_id"])
        if event:
            event["available_seats"] += booking["seats"]
        self.bookings = [b for b in self.bookings if b["id"] != booking_id]
