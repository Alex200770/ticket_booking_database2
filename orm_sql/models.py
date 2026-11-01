from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("btrim(title) <> ''", name="ck_events_title_not_blank"),
        CheckConstraint("btrim(venue) <> ''", name="ck_events_venue_not_blank"),
    )
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(150))
    venue = mapped_column(String(150))
    starts_at = mapped_column(DateTime)

    seats = relationship("Seat", back_populates="event")


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        CheckConstraint("row_number > 0", name="ck_seats_row_positive"),
        CheckConstraint("seat_number > 0", name="ck_seats_number_positive"),
        UniqueConstraint("event_id", "row_number", "seat_number", name="uq_seats_event_row_number"),
    )

    id = mapped_column(Integer, primary_key=True)
    event_id = mapped_column(
        Integer, ForeignKey("events.id", name="fk_seats_event", ondelete="CASCADE")
    )
    row_number = mapped_column(Integer)
    seat_number = mapped_column(Integer)

    event = relationship("Event", back_populates="seats")
    ticket = relationship("Ticket", back_populates="seat", uselist=False, passive_deletes="all")


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("seat_id", name="uq_tickets_seat"),
        CheckConstraint("btrim(customer_name) <> ''", name="ck_tickets_customer_not_blank"),
    )

    id = mapped_column(Integer, primary_key=True)
    seat_id = mapped_column(
        Integer, ForeignKey("seats.id", name="fk_tickets_seat", ondelete="RESTRICT")
    )
    customer_name = mapped_column(String(100))

    seat = relationship("Seat", back_populates="ticket")