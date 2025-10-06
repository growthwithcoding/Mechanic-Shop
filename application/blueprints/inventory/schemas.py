# application/blueprints/inventory/schemas.py
from marshmallow import fields, validate

from application.extensions import ma
from application.models import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    """Schema for Inventory model"""
    
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True
    
    # Add validation for fields
    name = fields.Str(required=True, validate=validate.Length(min=1, max=160))
    price = fields.Float(required=True, validate=validate.Range(min=0))


# Schema instances
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
