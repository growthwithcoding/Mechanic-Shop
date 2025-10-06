# application/blueprints/inventory/routes.py
from http import HTTPStatus
from flask import request, jsonify
from application.extensions import db, limiter, cache
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from application.models import Inventory


@inventory_bp.post("/")
@limiter.limit("10 per hour")  # Rate limiting: Prevents abuse by limiting inventory creation
def create_inventory():
    """Create a new inventory part"""
    inventory = inventory_schema.load(request.json or {})
    db.session.add(inventory)
    db.session.commit()
    return inventory_schema.jsonify(inventory), HTTPStatus.CREATED


@inventory_bp.get("/")
@cache.cached(timeout=60)  # Caching: Stores the list of inventory for 60 seconds
def list_inventory():
    """Get all inventory parts"""
    inventory_items = db.session.query(Inventory).all()
    return inventories_schema.jsonify(inventory_items), HTTPStatus.OK


@inventory_bp.get("/<int:inventory_id>")
def get_inventory(inventory_id):
    """Get a specific inventory part by ID"""
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), HTTPStatus.NOT_FOUND
    return inventory_schema.jsonify(inventory), HTTPStatus.OK


@inventory_bp.put("/<int:inventory_id>")
def update_inventory(inventory_id):
    """Update an existing inventory part"""
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), HTTPStatus.NOT_FOUND
    
    data = request.get_json() or {}
    for key, value in data.items():
        if hasattr(inventory, key):
            setattr(inventory, key, value)
    
    db.session.commit()
    return inventory_schema.jsonify(inventory), HTTPStatus.OK


@inventory_bp.delete("/<int:inventory_id>")
def delete_inventory(inventory_id):
    """Delete an inventory part"""
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), HTTPStatus.NOT_FOUND
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f"Inventory part {inventory_id} deleted"}), HTTPStatus.OK
