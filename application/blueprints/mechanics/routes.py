# application/blueprints/mechanics/routes.py
from http import HTTPStatus
from flask import request, jsonify
from ...extensions import db, limiter, cache
from . import mechanics_bp
from .schemas import MechanicSchema
from ...models import Mechanic

mech_schema = MechanicSchema()
mechs_schema = MechanicSchema(many=True)

@mechanics_bp.post("/")
@limiter.limit("5 per hour")  # Rate limiting: Prevents abuse by limiting mechanic creation to 5 per hour per IP
def create_mechanic():
    data = mech_schema.load(request.json or {})
    mech = Mechanic(**data)
    db.session.add(mech)
    db.session.commit()
    return mech_schema.jsonify(mech), HTTPStatus.CREATED

@mechanics_bp.get("/")
@cache.cached(timeout=60)  # Caching: Stores the list of mechanics for 60 seconds to reduce database queries
def list_mechanics():
    return mechs_schema.jsonify(db.session.query(Mechanic).all()), HTTPStatus.OK

@mechanics_bp.get("/<int:mechanic_id>")
def get_mechanic(mechanic_id):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error":"not found"}), HTTPStatus.NOT_FOUND
    return mech_schema.jsonify(mech), HTTPStatus.OK

@mechanics_bp.put("/<int:mechanic_id>")
def update_mechanic(mechanic_id):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error":"not found"}), HTTPStatus.NOT_FOUND
    data = (request.get_json() or {})
    for k, v in data.items():
        setattr(mech, k, v)
    db.session.commit()
    return mech_schema.jsonify(mech), HTTPStatus.OK

@mechanics_bp.delete("/<int:mechanic_id>")
def delete_mechanic(mechanic_id):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error":"not found"}), HTTPStatus.NOT_FOUND
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"mechanic {mechanic_id} deleted"}), HTTPStatus.OK

# Assignment 8: Get mechanics sorted by most tickets worked
@mechanics_bp.get("/most-active")
def get_most_active_mechanics():
    """
    Returns mechanics sorted by number of tickets worked (descending).
    Uses lambda function to sort by length of tickets relationship.
    This endpoint leverages the many-to-many relationship between mechanics and tickets.
    """
    mechanics = list(db.session.scalars(db.select(Mechanic)).all())
    
    # Sort mechanics by ticket count (descending order - most active first)
    mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
    
    # Create response with ticket counts for transparency
    result = [
        {
            "mechanic_id": m.mechanic_id,
            "full_name": m.full_name,
            "email": m.email,
            "tickets_worked": len(m.tickets),
            "is_active": m.is_active
        }
        for m in mechanics
    ]
    
    return jsonify(result), HTTPStatus.OK
