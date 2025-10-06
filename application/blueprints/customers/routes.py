# application/blueprints/customers/routes.py
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from application.blueprints.customers import customers_bp
from application.models import Customer, ServiceTicket
from application.extensions import db
from application.utils.util import encode_token, token_required
from .schemas import (
    customer_schema,
    customer_response_schema,
    customers_response_schema,
    login_schema,
    service_tickets_response_schema
)


@customers_bp.route('/register', methods=['POST'])
def register_customer():
    """
    Register a new customer (create account)
    
    Required fields:
    - first_name
    - last_name
    - email
    - password (min 6 characters)
    """
    try:
        # Validate and deserialize input
        if not request.json:
            return jsonify({'message': 'Request body is required'}), 400
        
        customer_data = customer_schema.load(request.json)
        
        # Check if email already exists
        existing_customer = db.session.execute(
            select(Customer).where(Customer.email == customer_data.email)
        ).scalar_one_or_none()
        
        if existing_customer:
            return jsonify({'message': 'Email already registered'}), 409
        
        # Add new customer to database
        db.session.add(customer_data)
        db.session.commit()
        
        # Return customer data without password
        return jsonify({
            'message': 'Customer registered successfully',
            'customer': customer_response_schema.dump(customer_data)
        }), 201
        
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating customer: {str(e)}'}), 500


@customers_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint - validates credentials and returns JWT token
    
    Required fields:
    - email
    - password
    
    Returns:
    - auth_token: JWT token for authentication
    """
    try:
        # Validate login credentials
        if not request.json:
            return jsonify({'message': 'Request body is required'}), 400
        
        credentials = login_schema.load(request.json)
        
        # Extract email and password from validated credentials
        if isinstance(credentials, dict):
            email = str(credentials.get('email', ''))
            password = str(credentials.get('password', ''))
        else:
            return jsonify({'message': 'Invalid credentials format'}), 400
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Query database for user with this email
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()
    
    # Validate customer exists and password matches
    if customer and customer.password == password:
        # Generate token
        auth_token = encode_token(customer.customer_id)
        
        response = {
            "status": "success",
            "message": "Successfully logged in",
            "auth_token": auth_token,
            "customer": customer_response_schema.dump(customer)
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': "Invalid email or password"}), 401


@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    """
    Get all service tickets for the authenticated customer
    
    Requires: Bearer token in Authorization header
    
    Returns all tickets associated with the customer's ID from the token
    """
    try:
        # Query tickets for this customer
        query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
        tickets = db.session.execute(query).scalars().all()
        
        # Manually serialize tickets to avoid relationship issues
        tickets_data = []
        for ticket in tickets:
            ticket_dict = {
                'ticket_id': ticket.ticket_id,
                'vehicle_id': ticket.vehicle_id,
                'customer_id': ticket.customer_id,
                'status': ticket.status,
                'opened_at': ticket.opened_at.isoformat() if ticket.opened_at else None,
                'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                'problem_description': ticket.problem_description,
                'odometer_miles': ticket.odometer_miles,
                'priority': ticket.priority
            }
            tickets_data.append(ticket_dict)
        
        return jsonify({
            'customer_id': customer_id,
            'ticket_count': len(tickets),
            'tickets': tickets_data
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error retrieving tickets: {str(e)}'}), 500


@customers_bp.route('/profile', methods=['GET'])
@token_required
def get_my_profile(customer_id):
    """
    Get the authenticated customer's profile information
    
    Requires: Bearer token in Authorization header
    """
    try:
        customer = db.session.get(Customer, customer_id)
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        return jsonify(customer_response_schema.dump(customer)), 200
        
    except Exception as e:
        return jsonify({'message': f'Error retrieving profile: {str(e)}'}), 500


@customers_bp.route('/profile', methods=['PUT'])
@token_required
def update_my_profile(customer_id):
    """
    Update the authenticated customer's profile
    
    Requires: Bearer token in Authorization header
    
    Allowed updates: first_name, last_name, phone, address fields
    Note: Email and password updates require separate endpoints for security
    """
    try:
        customer = db.session.get(Customer, customer_id)
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        # Get update data
        update_data = request.json
        
        if not update_data:
            return jsonify({'message': 'Request body is required'}), 400
        
        # Allowed fields for update
        allowed_fields = ['first_name', 'last_name', 'phone', 'address_line1', 
                         'address_line2', 'city', 'state', 'postal_code']
        
        # Update only allowed fields
        for field in allowed_fields:
            if field in update_data:
                setattr(customer, field, update_data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'customer': customer_response_schema.dump(customer)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating profile: {str(e)}'}), 500


@customers_bp.route('/profile', methods=['DELETE'])
@token_required
def delete_my_account(customer_id):
    """
    Delete the authenticated customer's account
    
    Requires: Bearer token in Authorization header
    
    Note: This will cascade delete all associated vehicles and may affect service tickets
    """
    try:
        customer = db.session.get(Customer, customer_id)
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully deleted account for customer {customer_id}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting account: {str(e)}'}), 500


@customers_bp.route('/', methods=['GET'])
def list_customers():
    """
    List all customers with pagination support (Assignment 8)
    
    Query params: 
    - page (default 1): Page number
    - per_page (default 10, max 100): Results per page
    
    Returns customers without password information plus pagination metadata
    """
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        # Calculate offset for pagination
        offset = (page - 1) * per_page
        
        # Query customers with limit and offset
        customers = db.session.execute(
            select(Customer)
            .order_by(Customer.customer_id)
            .limit(per_page)
            .offset(offset)
        ).scalars().all()
        
        # Get total count for pagination metadata
        total_count = db.session.execute(
            select(db.func.count(Customer.customer_id))
        ).scalar() or 0
        
        # Calculate total pages
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 0
        
        return jsonify({
            "customers": customers_response_schema.dump(customers),
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error retrieving customers: {str(e)}'}), 500


@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """
    Get a specific customer by ID (admin function - could be protected in production)
    """
    try:
        customer = db.session.get(Customer, customer_id)
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        return jsonify(customer_response_schema.dump(customer)), 200
        
    except Exception as e:
        return jsonify({'message': f'Error retrieving customer: {str(e)}'}), 500
