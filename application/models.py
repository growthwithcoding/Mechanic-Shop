# application/models.py
from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, SmallInteger, Text, ForeignKey,
    Boolean, Date, DateTime, Numeric,
    CheckConstraint, UniqueConstraint
)

from .extensions import db

Base = db.Model


# ---- Customers Table ----
class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(40))
    address_line1: Mapped[Optional[str]] = mapped_column(String(255))
    address_line2: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(120))
    state: Mapped[Optional[str]] = mapped_column(String(32))
    postal_code: Mapped[Optional[str]] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="customer", cascade="all, delete-orphan")
    tickets: Mapped[List["ServiceTicket"]] = relationship(back_populates="customer")


# ---- Vehicles Table ----
class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = (UniqueConstraint("vin", name="uq_vehicles_vin"),)

    vehicle_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    vin: Mapped[str] = mapped_column(String(32), nullable=False)
    make: Mapped[Optional[str]] = mapped_column(String(120))
    model: Mapped[Optional[str]] = mapped_column(String(120))
    year: Mapped[Optional[int]] = mapped_column(Integer)
    color: Mapped[Optional[str]] = mapped_column(String(64))

    customer: Mapped["Customer"] = relationship(back_populates="vehicles")
    tickets: Mapped[List["ServiceTicket"]] = relationship(back_populates="vehicle")


# ---- Mechanics Table ----
class Mechanic(Base):
    __tablename__ = "mechanics"
    __table_args__ = (
        UniqueConstraint("email", name="uq_mechanics_email"),
        CheckConstraint("salary_cents >= 0", name="ck_mechanics_salary_nonneg"),
    )

    mechanic_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(40))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    salary_cents: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    assignments: Mapped[List["TicketMechanic"]] = relationship(back_populates="mechanic", cascade="all, delete-orphan")
    tickets: Mapped[List["ServiceTicket"]] = relationship(
        secondary="ticket_mechanics", back_populates="mechanics", viewonly=True
    )


# ---- Service Tickets Table ----
class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    __table_args__ = (
        CheckConstraint("priority BETWEEN 1 AND 5", name="ck_tickets_priority_1_5"),
        CheckConstraint("status in ('OPEN','IN_PROGRESS','COMPLETED','CANCELLED')", name="ck_tickets_status"),
    )

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.vehicle_id", ondelete="RESTRICT"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="OPEN", nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    problem_description: Mapped[Optional[str]] = mapped_column(Text)
    odometer_miles: Mapped[Optional[int]] = mapped_column(Integer)
    priority: Mapped[Optional[int]] = mapped_column(SmallInteger)

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="tickets")
    line_items: Mapped[List["TicketLineItem"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")
    assignments: Mapped[List["TicketMechanic"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")
    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary="ticket_mechanics", back_populates="tickets", viewonly=True
    )


# ---- Services Table ----
class Service(Base):
    __tablename__ = "services"
    __table_args__ = (
        UniqueConstraint("name", name="uq_services_name"),
        CheckConstraint("base_price_cents >= 0", name="ck_services_price_nonneg"),
    )

    service_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    default_labor_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    base_price_cents: Mapped[Optional[int]] = mapped_column(Integer)

    line_items: Mapped[List["TicketLineItem"]] = relationship(back_populates="service")


# ---- Ticket Line Items Table ----
class TicketLineItem(Base):
    __tablename__ = "ticket_line_items"
    __table_args__ = (
        CheckConstraint("unit_price_cents >= 0", name="ck_lineitems_price_nonneg"),
        CheckConstraint("line_type in ('LABOR','PART','SERVICE')", name="ck_lineitems_type"),
    )

    line_item_id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.ticket_id", ondelete="CASCADE"), nullable=False)
    service_id: Mapped[Optional[int]] = mapped_column(ForeignKey("services.service_id"))
    line_type: Mapped[str] = mapped_column(String(16), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(10, 2), default=1)
    unit_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    ticket: Mapped["ServiceTicket"] = relationship(back_populates="line_items")
    service: Mapped[Optional["Service"]] = relationship(back_populates="line_items")


# ---- Ticket ↔ Mechanic Junction Table ----
class TicketMechanic(Base):
    __tablename__ = "ticket_mechanics"
    __table_args__ = (
        CheckConstraint("minutes_worked >= 0", name="ck_tm_minutes_nonneg"),
        CheckConstraint("role in ('LEAD','ASSIST')", name="ck_tm_role"),
    )

    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.ticket_id", ondelete="CASCADE"), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanics.mechanic_id", ondelete="RESTRICT"), primary_key=True)
    role: Mapped[str] = mapped_column(String(16), default="ASSIST", nullable=False)
    minutes_worked: Mapped[int] = mapped_column(Integer, default=0)

    ticket: Mapped["ServiceTicket"] = relationship(back_populates="assignments")
    mechanic: Mapped["Mechanic"] = relationship(back_populates="assignments")
