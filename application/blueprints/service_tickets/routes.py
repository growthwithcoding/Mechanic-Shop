from http import HTTPStatus
from flask import request
from ...extensions import db
from ...models import ServiceTicket, Mechanic
from .schemas import service_ticket_schema, service_tickets_schema
from . import service_tickets_bp

# List all service tickets
@service_tickets_bp.get("/")
def list_tickets():
    tickets = db.session.scalars(
        db.select(ServiceTicket).order_by(ServiceTicket.ticket_id)
    ).all()
    return service_tickets_schema.jsonify(tickets), HTTPStatus.OK

# Create a new service ticket
@service_tickets_bp.post("/")
def create_ticket():
    payload = request.get_json() or {}
    ticket = ServiceTicket(**payload)
    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), HTTPStatus.CREATED

# Assign a mechanic to a ticket
@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id: int, mechanic_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mech = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mech:
        return {"error": "Ticket or Mechanic not found."}, HTTPStatus.NOT_FOUND
    if mech not in ticket.mechanics:
        ticket.mechanics.append(mech)
    db.session.commit()
    return {"message": f"Mechanic {mechanic_id} assigned to Ticket {ticket_id}."}, HTTPStatus.OK

# Remove a mechanic from a ticket
@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id: int, mechanic_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mech = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mech:
        return {"error": "Ticket or Mechanic not found."}, HTTPStatus.NOT_FOUND
    if mech in ticket.mechanics:
        ticket.mechanics.remove(mech)
    db.session.commit()
    return {"message": f"Mechanic {mechanic_id} removed from Ticket {ticket_id}."}, HTTPStatus.OK
