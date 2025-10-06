"""
inspect_db_contents.py
Coding Temple – Backend Module 1, Lesson 2
Mechanic Shop – Verify seeded data & relationships (read-only)

Purpose:
    Connects to the same DB configured in .env and prints a concise snapshot:
      - table counts
      - customers with their vehicles
      - tickets with customer, vehicle, mechanics, and line items

Usage:
    1) Ensure .env has APP_DATABASE_URI set (same as create_db_tables.py)
    2) python inspect_db_contents.py
"""
from __future__ import annotations
from typing import Iterable

from create_db_tables import (
    app, db,
    Customer, Vehicle, Mechanic, Service, ServiceTicket, TicketLineItem, TicketMechanic
)


def _hr(title: str = "") -> None:
    line = "=" * 72
    if title:
        print(f"\n{line}\n{title}\n{line}")
    else:
        print(f"\n{line}")


def _print_rows(label: str, rows: Iterable, limit: int = 10) -> None:
    print(f"\n{label} (showing up to {limit})")
    count = 0
    for r in rows:
        print("  •", r)
        count += 1
        if count >= limit:
            break
    if count == 0:
        print("  (none)")


def _ticket_summary(t: ServiceTicket) -> str:
    mech_names = [tm.mechanic.full_name for tm in t.assignments]
    return (
        f"Ticket #{t.ticket_id} | status={t.status} | priority={t.priority} | "
        f"customer={t.customer.last_name}, {t.customer.first_name} | "
        f"vehicle VIN={t.vehicle.vin} | mechanics={', '.join(mech_names) if mech_names else '—'}"
    )


def _line_item_summary(li: TicketLineItem) -> str:
    return (
        f"LineItem #{li.line_item_id} | {li.line_type} | qty={li.quantity} | "
        f"unit_cents={li.unit_price_cents} | desc={li.description[:60]}"
    )


if __name__ == "__main__":
    with app.app_context():
        _hr("DATABASE SNAPSHOT – COUNTS")
        customer_count = db.session.scalar(db.select(db.func.count()).select_from(Customer))
        vehicle_count = db.session.scalar(db.select(db.func.count()).select_from(Vehicle))
        mech_count = db.session.scalar(db.select(db.func.count()).select_from(Mechanic))
        service_count = db.session.scalar(db.select(db.func.count()).select_from(Service))
        ticket_count = db.session.scalar(db.select(db.func.count()).select_from(ServiceTicket))
        line_item_count = db.session.scalar(db.select(db.func.count()).select_from(TicketLineItem))
        tm_count = db.session.scalar(db.select(db.func.count()).select_from(TicketMechanic))

        print(f"Customers:        {customer_count}")
        print(f"Vehicles:         {vehicle_count}")
        print(f"Mechanics:        {mech_count}")
        print(f"Services:         {service_count}")
        print(f"Service Tickets:  {ticket_count}")
        print(f"Line Items:       {line_item_count}")
        print(f"Ticket↔Mechanic:  {tm_count}")

        _hr("CUSTOMERS WITH VEHICLES")
        customers = db.session.scalars(db.select(Customer).order_by(Customer.customer_id)).all()
        if not customers:
            print("No customers found. Did you run create_db_tables.py and seed_demo_data()?")
        for c in customers:
            print(f"\nCustomer #{c.customer_id}: {c.last_name}, {c.first_name} <{c.email}>")
            if c.vehicles:
                for v in c.vehicles:
                    print(f"  - Vehicle #{v.vehicle_id}: VIN={v.vin} {v.make or ''} {v.model or ''} {v.year or ''}")
            else:
                print("  (no vehicles)")

        _hr("TICKETS – SUMMARY")
        tickets = db.session.scalars(
            db.select(ServiceTicket).order_by(ServiceTicket.ticket_id)
        ).all()
        if not tickets:
            print("No tickets found. Seed data may be disabled.")
        for t in tickets:
            print("\n", _ticket_summary(t))
            if t.line_items:
                for li in t.line_items:
                    print("   •", _line_item_summary(li))
            else:
                print("   (no line items)")

        _hr("MECHANIC WORKLOAD (minutes by ticket)")
        mechanics = db.session.scalars(db.select(Mechanic).order_by(Mechanic.mechanic_id)).all()
        if not mechanics:
            print("No mechanics found.")
        for m in mechanics:
            total_minutes = sum(tm.minutes_worked for tm in m.assignments)
            print(f"\nMechanic #{m.mechanic_id}: {m.full_name} | total minutes: {total_minutes}")
            if m.assignments:
                for tm in m.assignments:
                    print(f"   - Ticket #{tm.ticket_id}: role={tm.role} minutes={tm.minutes_worked}")
            else:
                print("   (no assignments)")

        _hr()
        print("✅ Inspection complete.")