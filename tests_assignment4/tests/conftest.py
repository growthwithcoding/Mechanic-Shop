import os
import pytest
from application import create_app
from application.extensions import db

@pytest.fixture(scope="session")
def app():
    # Force testing config + in-memory SQLite for isolation and speed
    os.environ["FLASK_CONFIG"] = "testing"
    app = create_app("testing")
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with app.app_context():
        db.create_all()
    yield app
    # No teardown needed for in-memory DB

@pytest.fixture()
def client(app):
    """Provides a test client with a clean database for each test."""
    with app.app_context():
        # Clean all tables before each test
        db.session.remove()
        db.drop_all()
        db.create_all()
    return app.test_client()
