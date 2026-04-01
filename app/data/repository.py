from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


DB_PATH = Path(__file__).resolve().parents[2] / "event_booking.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    available_seats: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="event")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped[User] = relationship(back_populates="bookings")
    event: Mapped[Event] = relationship(back_populates="bookings")


class Repository:
    _instance: ClassVar["Repository" | None] = None

    def __init__(self) -> None:
        Base.metadata.create_all(ENGINE)
        self._ensure_seed_data()

    @classmethod
    def get_instance(cls) -> "Repository":
        if cls._instance is None:
            cls._instance = Repository()
        return cls._instance

    def _ensure_seed_data(self) -> None:
        with Session(ENGINE) as session:
            if not session.query(User).first():
                session.add_all(
                    [
                        User(username="student1", password="password"),
                        User(username="admin", password="admin"),
                    ]
                )
            if not session.query(Event).first():
                session.add_all(
                    [
                        Event(name="Tech Talk", available_seats=50),
                        Event(name="Workshop", available_seats=30),
                    ]
                )
            session.commit()

    # User operations
    def get_user_by_username(self, username: str) -> User | None:
        with Session(ENGINE) as session:
            return session.query(User).filter_by(username=username).first()

    # Event operations
    def search_events(self, keyword: str | None = None) -> list[Event]:
        with Session(ENGINE) as session:
            query = session.query(Event)
            if keyword:
                kw = f"%{keyword.lower()}%"
                query = query.filter(Event.name.ilike(kw))
            return query.order_by(Event.id).all()

    def get_event_by_id(self, event_id: int) -> Event | None:
        with Session(ENGINE) as session:
            return session.query(Event).get(event_id)

    # Booking operations
    def create_booking(self, username: str, event_id: int, seats: int) -> Booking:
        with Session(ENGINE) as session:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                raise ValueError("User not found")

            event = session.query(Event).get(event_id)
            if not event:
                raise ValueError("Event not found")
            if event.available_seats < seats:
                raise ValueError("No seats available")

            event.available_seats -= seats
            booking = Booking(user=user, event=event, seats=seats)
            session.add(booking)
            session.commit()
            session.refresh(booking)
            return booking

    def get_booking_by_id(self, booking_id: int) -> Booking | None:
        with Session(ENGINE) as session:
            return session.query(Booking).get(booking_id)

    def cancel_booking(self, booking_id: int) -> None:
        with Session(ENGINE) as session:
            booking = session.query(Booking).get(booking_id)
            if not booking:
                raise ValueError("Booking not found")
            event = booking.event
            event.available_seats += booking.seats
            session.delete(booking)
            session.commit()

    def get_bookings_for_user(self, username: str) -> list[Booking]:
        with Session(ENGINE) as session:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return []
            return (
                session.query(Booking)
                .filter_by(user_id=user.id)
                .join(Event)
                .order_by(Booking.id)
                .all()
            )

