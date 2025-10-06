import os
import pytest
from application import create_app
from application.extensions import db
from application.models import Customer, Vehicle

@pytest.fixture(scope="session")
def app():
    os.environ.setdefault(
        "APP_DATABASE_URI",
        "mysql+mysqlconnector://mechanic_user:MySecurePassword123@127.0.0.1/mechanic_shop"
    )
    app = create_app("testing")
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    """Provides a test client for making HTTP requests."""
    return app.test_client()

@pytest.fixture(autouse=True)
def _clean_db(app):
    """Clean database before each test."""
    with app.app_context():
        # Clean up before the test runs
        db.session.rollback()
        # Delete all records from tables
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
    
    yield
    
    with app.app_context():
        # Clean up after the test runs
        db.session.rollback()

def seed_basic_customer_vehicle():
    """
    Seeds a basic customer with customer_id=1 and a vehicle with vehicle_id=1.
    This is used by tests that need existing customer and vehicle data.
    """
    # Check if customer already exists
    existing_customer = db.session.get(Customer, 1)
    if not existing_customer:
        customer = Customer()
        customer.customer_id = 1
        customer.first_name = "Test"
        customer.last_name = "Customer"
        customer.email = "test@customer.local"
        customer.phone = "555-1234"
        db.session.add(customer)
    
    # Check if vehicle already exists
    existing_vehicle = db.session.get(Vehicle, 1)
    if not existing_vehicle:
        vehicle = Vehicle()
        vehicle.vehicle_id = 1
        vehicle.customer_id = 1
        vehicle.vin = "TEST123VIN456"
        vehicle.make = "Test"
        vehicle.model = "Model"
        vehicle.year = 2020
        db.session.add(vehicle)
    
    db.session.commit()
