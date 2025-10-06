"""
app.py – Assignment 3 (Lesson 3)
Mechanic Shop – RESTful API with Marshmallow Schemas (Flask + SQLAlchemy)

Purpose:
    Expose CRUD endpoints for the Mechanic Shop database using Flask.
    Use Marshmallow to validate input (deserialization) and serialize model instances to JSON.

Prereqs:
    - Database and models created in Assignment 2 (create_db_tables.py)
    - .env has APP_DATABASE_URI set (same as before)
    - pip install flask-marshmallow marshmallow-sqlalchemy

Run:
    python app.py
    # Then test endpoints, e.g.:
    # GET  http://127.0.0.1:5000/health
    # GET  http://127.0.0.1:5000/customers
"""

from __future__ import annotations
from http import HTTPStatus

from flask import request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, fields, validate

# Reuse the configured Flask app, db, and models from Assignment 2
from create_db_tables import (
    app as base_app, db,
    Customer, Vehicle, Mechanic, Service, ServiceTicket, TicketLineItem, TicketMechanic
)

# Use the same Flask app instance from create_db_tables.py
app = base_app

# Initialize Marshmallow
ma = Marshmallow(app)


# ============================
#   Marshmallow Schemas
# ============================

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = False  # We will construct model manually in POST/PUT
        ordered = True

    customer_id = ma.auto_field(dump_only=True)
    first_name = ma.auto_field(required=True, validate=validate.Length(min=1, max=120))
    last_name  = ma.auto_field(required=True, validate=validate.Length(min=1, max=120))
    email      = ma.auto_field(required=True, validate=validate.Email())
    phone        = ma.auto_field(load_default=None)
    address_line1= ma.auto_field(load_default=None)
    address_line2= ma.auto_field(load_default=None)
    city         = ma.auto_field(load_default=None)
    state        = ma.auto_field(load_default=None)
    postal_code  = ma.auto_field(load_default=None)
    created_at   = ma.auto_field(dump_only=True)

    # Read-only vehicle preview via Method field
    vehicles = fields.Method("get_vehicle_preview", dump_only=True)

    def get_vehicle_preview(self, obj):
        return [
            {
                "vehicle_id": v.vehicle_id,
                "vin": v.vin,
                "make": v.make,
                "model": v.model,
                "year": v.year,
            }
            for v in obj.vehicles
        ]


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


# ============================
#   Helpers
# ============================

def _unique_email(email: str, exclude_customer_id: int | None = None) -> bool:
    q = db.select(Customer).where(Customer.email == email)
    if exclude_customer_id is not None:
        q = q.where(Customer.customer_id != exclude_customer_id)
    exists = db.session.execute(q).scalars().first()
    return exists is None


# ============================
#   Routes
# ============================

@app.get("/health")
def health() -> tuple[dict, int]:
    return {"status": "ok"}, HTTPStatus.OK


# ---- Customers ----

@app.get("/customers")
def list_customers():
    customers = db.session.scalars(db.select(Customer).order_by(Customer.customer_id)).all()
    return customers_schema.jsonify(customers), HTTPStatus.OK


@app.get("/customers/<int:customer_id>")
def get_customer(customer_id: int):
    c = db.session.get(Customer, customer_id)
    if not c:
        return {"error": "Customer not found."}, HTTPStatus.NOT_FOUND
    return customer_schema.jsonify(c), HTTPStatus.OK


@app.post("/customers")
def create_customer():
    try:
        payload = customer_schema.load(request.get_json() or {})
    except ValidationError as err:
        return {"errors": err.messages}, HTTPStatus.BAD_REQUEST

    if not _unique_email(payload["email"]):
        return {"error": "Email already associated with an account."}, HTTPStatus.BAD_REQUEST

    c = Customer(**payload)
    db.session.add(c)
    db.session.commit()
    return customer_schema.jsonify(c), HTTPStatus.CREATED


@app.put("/customers/<int:customer_id>")
def update_customer(customer_id: int):
    c = db.session.get(Customer, customer_id)
    if not c:
        return {"error": "Customer not found."}, HTTPStatus.NOT_FOUND

    try:
        payload = customer_schema.load(request.get_json() or {})
    except ValidationError as err:
        return {"errors": err.messages}, HTTPStatus.BAD_REQUEST

    if "email" in payload and not _unique_email(payload["email"], exclude_customer_id=customer_id):
        return {"error": "Email already associated with an account."}, HTTPStatus.BAD_REQUEST

    for key, value in payload.items():
        setattr(c, key, value)

    db.session.commit()
    return customer_schema.jsonify(c), HTTPStatus.OK


@app.delete("/customers/<int:customer_id>")
def delete_customer(customer_id: int):
    c = db.session.get(Customer, customer_id)
    if not c:
        return {"error": "Customer not found."}, HTTPStatus.NOT_FOUND
    db.session.delete(c)
    db.session.commit()
    return {"message": f"Customer id {customer_id} deleted."}, HTTPStatus.OK


# ============================
#   Entrypoint
# ============================

if __name__ == "__main__":
    # For classroom/demo use only
    app.run(host="127.0.0.1", port=5000, debug=True)
