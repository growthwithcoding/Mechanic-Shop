from application.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customers'
    
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    city: Mapped[str] = mapped_column(db.String(100), nullable=False)
    state: Mapped[str] = mapped_column(db.String(50), nullable=False)
    postal_code: Mapped[str] = mapped_column(db.String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    vehicles: Mapped[List['Vehicle']] = db.relationship(back_populates='customer')
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    vehicle_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.customer_id'), nullable=False)
    vin: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    make: Mapped[str] = mapped_column(db.String(100), nullable=False)
    model: Mapped[str] = mapped_column(db.String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(db.String(50), nullable=False)
    
    # Relationships
    customer: Mapped['Customer'] = db.relationship(back_populates='vehicles')
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='vehicle')


class Mechanic(db.Model):
    __tablename__ = 'mechanics'
    
    mechanic_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    salary: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    
    # Relationships
    ticket_mechanics: Mapped[List['TicketMechanic']] = db.relationship(back_populates='mechanic')


class Service(db.Model):
    __tablename__ = 'services'
    
    service_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    default_labor_minutes: Mapped[int] = mapped_column(nullable=False)
    base_price_cents: Mapped[int] = mapped_column(nullable=False)
    
    # Relationships
    ticket_line_items: Mapped[List['TicketLineItem']] = db.relationship(back_populates='service')


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'
    
    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey('vehicles.vehicle_id'), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.customer_id'), nullable=False)
    status: Mapped[str] = mapped_column(db.String(50), nullable=False)
    opened_at: Mapped[datetime] = mapped_column(db.TIMESTAMP, default=datetime.utcnow)
    closed_at: Mapped[datetime] = mapped_column(db.TIMESTAMP, nullable=True)
    problem_description: Mapped[str] = mapped_column(db.Text, nullable=False)
    odometer_miles: Mapped[int] = mapped_column(nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)
    
    # Relationships
    vehicle: Mapped['Vehicle'] = db.relationship(back_populates='service_tickets')
    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    ticket_line_items: Mapped[List['TicketLineItem']] = db.relationship(back_populates='service_ticket')
    ticket_mechanics: Mapped[List['TicketMechanic']] = db.relationship(back_populates='service_ticket')


class TicketLineItem(db.Model):
    __tablename__ = 'ticket_line_items'
    
    line_item_id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.ticket_id'), nullable=False)
    service_id: Mapped[int] = mapped_column(db.ForeignKey('services.service_id'), nullable=False)
    line_type: Mapped[str] = mapped_column(db.String(50), nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)
    quantity: Mapped[float] = mapped_column(db.Numeric(10, 2), nullable=False)
    unit_price_cents: Mapped[int] = mapped_column(nullable=False)
    
    # Relationships
    service_ticket: Mapped['ServiceTicket'] = db.relationship(back_populates='ticket_line_items')
    service: Mapped['Service'] = db.relationship(back_populates='ticket_line_items')


class TicketMechanic(db.Model):
    __tablename__ = 'ticket_mechanics'
    
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.ticket_id'), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.mechanic_id'), primary_key=True)
    role: Mapped[str] = mapped_column(db.String(100), nullable=False)
    minutes_worked: Mapped[int] = mapped_column(nullable=False)
    
    # Relationships
    service_ticket: Mapped['ServiceTicket'] = db.relationship(back_populates='ticket_mechanics')
    mechanic: Mapped['Mechanic'] = db.relationship(back_populates='ticket_mechanics')
