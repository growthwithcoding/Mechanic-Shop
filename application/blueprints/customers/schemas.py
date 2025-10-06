# application/blueprints/customers/schemas.py
from marshmallow import Schema, fields, validate, ValidationError, post_load

from application.extensions import ma
from application.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Customer model - includes password for creation"""
    
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
    
    # Add validation for fields
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=120))


class CustomerResponseSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Customer responses - excludes password"""
    
    class Meta:
        model = Customer
        exclude = ('password',)
        include_fk = True


class LoginSchema(Schema):
    """Schema for login credentials - only email and password"""
    
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))


class ServiceTicketResponseSchema(Schema):
    """Schema for service ticket responses"""
    
    ticket_id = fields.Int()
    vehicle_id = fields.Int()
    customer_id = fields.Int()
    status = fields.Str()
    opened_at = fields.DateTime()
    closed_at = fields.DateTime(allow_none=True)
    problem_description = fields.Str(allow_none=True)
    odometer_miles = fields.Int(allow_none=True)
    priority = fields.Int(allow_none=True)
    
    # Include vehicle information (optional)
    vehicle = fields.Nested('VehicleSchema', only=['vehicle_id', 'make', 'model', 'year', 'vin'], allow_none=True, required=False)
    
    # Include assigned mechanics (optional)
    mechanics = fields.Nested('MechanicSchema', many=True, only=['mechanic_id', 'full_name', 'email'], allow_none=True, required=False)


class VehicleSchema(Schema):
    """Schema for vehicle information"""
    
    vehicle_id = fields.Int()
    customer_id = fields.Int()
    vin = fields.Str()
    make = fields.Str()
    model = fields.Str()
    year = fields.Int()
    color = fields.Str()


class MechanicSchema(Schema):
    """Schema for mechanic information"""
    
    mechanic_id = fields.Int()
    full_name = fields.Str()
    email = fields.Email()
    phone = fields.Str()


# Schema instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_response_schema = CustomerResponseSchema()
customers_response_schema = CustomerResponseSchema(many=True)
login_schema = LoginSchema()
service_ticket_response_schema = ServiceTicketResponseSchema()
service_tickets_response_schema = ServiceTicketResponseSchema(many=True)
