from flask import Flask
from config import config
from application.extensions import db, ma


def create_app(config_name='default'):
    """
    Application Factory Pattern
    Creates and configures the Flask application instance
    
    Args:
        config_name (str): The configuration to use ('development', 'testing', 'production', 'default')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    from application.blueprints.customer import customer_bp
    app.register_blueprint(customer_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    return app
