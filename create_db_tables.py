"""
create_db_tables.py
Coding Temple – Backend Module 1, Lesson 2
Mechanic Shop – SQLAlchemy Models + Relationships (Flask + MySQL)

Purpose:
    Initialize the Mechanic Shop database tables using SQLAlchemy ORM.
    Creates all schema tables based on the ERD and seeds demo data for testing.

Usage (Windows / PowerShell):
    1) python -m venv venv
    2) .\venv\Scripts\activate
    3) pip install flask flask-sqlalchemy mysql-connector-python python-dotenv
    4) In MySQL Workbench:  CREATE DATABASE mechanic_shop;
    5) Create a .env file in this folder containing:
           APP_DATABASE_URI=mysql+mysqlconnector://mechanic_user:MySecurePassword123@127.0.0.1/mechanic_shop
    6) python create_db_tables.py
"""

from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, SmallInteger, Text, ForeignKey,
    Boolean, Date, DateTime, Numeric,
    CheckConstraint, UniqueConstraint
)
from dotenv import load_dotenv


# ===========================
#   App + Database Setup
# ===========================

# Load environment variables from .env
load_dotenv(override=True)


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Initialize SQLAlchemy (using 2.0 style)
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Require a valid connection string from .env
uri = os.getenv("APP_DATABASE_URI")
if not uri:
    raise RuntimeError("APP_DATABASE_URI not set in .env")

# Apply DB config to Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Display current DB connection info
user_segment = uri.split("//", 1)[1].split("@", 1)[0]
host_segment = uri.split("@", 1)[1].split("/", 1)[0]
print(f"Connecting as: {user_segment.split(':', 1)[0]}@{host_segment}")


# ===========================
#   ORM Models (Full ERD)
# ===========================

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
        secondary=lambda: TicketMechanic.__table__, back_populates="mechanics", viewonly=True
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
        secondary=lambda: TicketMechanic.__table__, back_populates="tickets", viewonly=True
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


# ===========================
#   Demo Data Seeder
# ===========================
def seed_demo_data():
    """Populate demo data for testing relationships and integrity."""
    c = Customer(first_name="Casey", last_name="Ng", email="casey@example.com", phone="555-201-2222")
    v = Vehicle(customer=c, vin="1HGCM82633A004352", make="Honda", model="Accord", year=2018, color="Blue")
    m1 = Mechanic(full_name="Avery Shah", email="avery@shop.local", salary_cents=6500000)
    m2 = Mechanic(full_name="Jordan Lee", email="jordan@shop.local", salary_cents=5200000)
    svc_brake = Service(name="Brake Pad Replacement", default_labor_minutes=120, base_price_cents=25000)

    t = ServiceTicket(customer=c, vehicle=v, status="IN_PROGRESS", problem_description="Brake squeal; oil change due",
                      odometer_miles=82310, priority=3)

    # Assign mechanics
    tm1 = TicketMechanic(ticket=t, mechanic=m1, role="LEAD", minutes_worked=45)
    tm2 = TicketMechanic(ticket=t, mechanic=m2, role="ASSIST", minutes_worked=25)

    # Line items
    li1 = TicketLineItem(ticket=t, line_type="SERVICE", description="Brake Pad Replacement",
                         quantity=1, unit_price_cents=25000, service=svc_brake)
    li2 = TicketLineItem(ticket=t, line_type="PART", description="Brake pads (front set)",
                         quantity=1, unit_price_cents=12000)
    li3 = TicketLineItem(ticket=t, line_type="LABOR", description="Additional diagnosis",
                         quantity=0.5, unit_price_cents=8000)

    db.session.add_all([c, v, m1, m2, svc_brake, t, tm1, tm2, li1, li2, li3])
    db.session.commit()


# ===========================
#   Bootstrap Execution
# ===========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Uncomment to populate seed data once
        # seed_demo_data()

    print("✅ Tables created for Mechanic Shop. Using .env connection URI.")
