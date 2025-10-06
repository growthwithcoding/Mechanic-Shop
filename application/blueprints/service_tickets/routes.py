from http import HTTPStatus
from flask import request
from ...extensions import db, limiter, cache
from ...models import ServiceTicket, Mechanic, Customer, Vehicle, Inventory, ServiceInventory
from .schemas import service_ticket_schema, service_tickets_schema
from . import service_tickets_bp

# List all service tickets
@service_tickets_bp.get("/")
@cache.cached(timeout=30)  # Caching: Stores ticket list for 30 seconds to reduce database load on frequently accessed endpoint
def list_tickets():
    tickets = db.session.scalars(
        db.select(ServiceTicket).order_by(ServiceTicket.ticket_id)
    ).all()
    return service_tickets_schema.jsonify(tickets), HTTPStatus.OK

# Create a new service ticket
@service_tickets_bp.post("/")
@limiter.limit("10 per hour")  # Rate limiting: Prevents spam by limiting ticket creation to 10 per hour per IP
def create_ticket():
    payload = request.get_json() or {}
    
    # Handle Postman-style input with customer/vehicle details
    customer_id = payload.get('customer_id')
    vehicle_id = payload.get('vehicle_id')
    
    # If customer_id not provided, try to create/find customer from provided details
    if not customer_id and 'customer_email' in payload:
        customer = db.session.scalars(
            db.select(Customer).where(Customer.email == payload['customer_email'])
        ).first()
        
        if not customer:
            # Split customer_name into first_name and last_name
            customer_name = payload.get('customer_name', 'Unknown Customer')
            name_parts = customer_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            customer = Customer(  # type: ignore[call-arg]
                first_name=first_name,
                last_name=last_name,
                email=payload['customer_email'],
                phone=payload.get('customer_phone')
            )
            db.session.add(customer)
            db.session.flush()  # Get customer_id without committing
        
        customer_id = customer.customer_id
    
    # If vehicle_id not provided, try to create vehicle from provided details
    if not vehicle_id and customer_id:
        # For simplicity, create a new vehicle with a generated VIN
        import random
        vin = f"VIN{random.randint(100000000, 999999999)}"
        
        vehicle = Vehicle(  # type: ignore[call-arg]
            customer_id=customer_id,
            vin=vin,
            make=payload.get('vehicle_make'),
            model=payload.get('vehicle_model'),
            year=payload.get('vehicle_year')
        )
        db.session.add(vehicle)
        db.session.flush()  # Get vehicle_id without committing
        vehicle_id = vehicle.vehicle_id
    
    # Map 'description' to 'problem_description' if provided
    problem_description = payload.get('problem_description') or payload.get('description')
    
    # Create the ticket with the proper IDs
    ticket = ServiceTicket(  # type: ignore[call-arg]
        customer_id=customer_id,
        vehicle_id=vehicle_id,
        problem_description=problem_description,
        status=payload.get('status', 'OPEN'),
        priority=payload.get('priority')
    )
    
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

# Assignment 8: Bulk edit mechanics on a ticket
@service_tickets_bp.put("/<int:ticket_id>/edit")
def edit_ticket_mechanics(ticket_id: int):
    """
    Bulk add/remove mechanics from a ticket.
    Accepts add_ids and remove_ids arrays in request body.
    Example: {"add_ids": [1, 2, 3], "remove_ids": [4, 5]}
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, HTTPStatus.NOT_FOUND
    
    payload = request.get_json() or {}
    add_ids = payload.get('add_ids', [])
    remove_ids = payload.get('remove_ids', [])
    
    # Remove mechanics first
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
    
    # Then add new mechanics
    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
    
    db.session.commit()
    
    return {
        "message": f"Ticket {ticket_id} mechanics updated",
        "mechanics": [m.mechanic_id for m in ticket.mechanics]
    }, HTTPStatus.OK


# Assignment 10: Add inventory part to a service ticket
@service_tickets_bp.post("/<int:ticket_id>/add-part/<int:inventory_id>")
def add_part_to_ticket(ticket_id: int, inventory_id: int):
    """
    Add a single inventory part to an existing service ticket.
    Creates a relationship between the ticket and the inventory part.
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, HTTPStatus.NOT_FOUND
    
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return {"error": "Inventory part not found"}, HTTPStatus.NOT_FOUND
    
    # Check if part is already added to this ticket
    if inventory in ticket.inventory_parts:
        return {"error": "Part already added to this ticket"}, HTTPStatus.BAD_REQUEST
    
    # Add the part to the ticket
    ticket.inventory_parts.append(inventory)
    db.session.commit()
    
    return {
        "message": f"Part '{inventory.name}' added to Ticket {ticket_id}",
        "ticket_id": ticket_id,
        "inventory_id": inventory_id,
        "part_name": inventory.name,
        "part_price": float(inventory.price)
    }, HTTPStatus.OK
