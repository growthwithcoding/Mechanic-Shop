# tests_assignment7/tests/conftest.py
import pytest
import os
from application import create_app
from application.extensions import db
from application.models import Customer, Vehicle, ServiceTicket


@pytest.fixture(scope="function")
def app():
    """Create and configure a test application instance."""
    # Set test database to in-memory SQLite
    os.environ['APP_DATABASE_URI'] = 'sqlite:///:memory:'
    
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture(scope="function")
def test_customer(app):
    """Create a test customer with password."""
    customer = Customer(
        first_name="Test",
        last_name="Customer",
        email="test@example.com",
        password="testpass123",
        phone="555-0001"
    )
    db.session.add(customer)
    db.session.commit()
    return customer


@pytest.fixture(scope="function")
def auth_token(client, test_customer):
    """Get an authentication token for the test customer."""
    response = client.post(
        '/customers/login',
        json={
            'email': test_customer.email,
            'password': 'testpass123'
        }
    )
    data = response.get_json()
    return data['auth_token']


@pytest.fixture(scope="function")
def test_vehicle(app, test_customer):
    """Create a test vehicle for the test customer."""
    vehicle = Vehicle(
        customer_id=test_customer.customer_id,
        vin="TEST123VIN456",
        make="Toyota",
        model="Camry",
        year=2020
    )
    db.session.add(vehicle)
    db.session.commit()
    return vehicle


@pytest.fixture(scope="function")
def test_ticket(app, test_customer, test_vehicle):
    """Create a test service ticket."""
    ticket = ServiceTicket(
        vehicle_id=test_vehicle.vehicle_id,
        customer_id=test_customer.customer_id,
        status="OPEN",
        problem_description="Oil change needed",
        priority=2
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket
