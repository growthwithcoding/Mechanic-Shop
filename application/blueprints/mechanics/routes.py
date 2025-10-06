# application/blueprints/mechanics/routes.py
from http import HTTPStatus
from flask import request, jsonify
from ...extensions import db
from . import mechanics_bp
from .schemas import MechanicSchema
from ...models import Mechanic

mech_schema = MechanicSchema()
mechs_schema = MechanicSchema(many=True)

@mechanics_bp.post("/")
def create_mechanic():
    data = mech_schema.load(request.json or {})
    mech = Mechanic(**data)
    db.session.add(mech)
    db.session.commit()
    return mech_schema.jsonify(mech), HTTPStatus.CREATED

@mechanics_bp.get("/")
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
