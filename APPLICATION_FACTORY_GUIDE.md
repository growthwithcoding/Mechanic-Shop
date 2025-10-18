# Application Factory Pattern - Mechanic Shop API

## Overview
This project has been refactored to use the **Application Factory Pattern**, which provides modularity, scalability, and support for multiple configurations.

## Project Structure

```
/Mechanic-Shop-V1
├── /application
│   ├── __init__.py              # Contains create_app() - Application Factory
│   ├── extensions.py            # Flask extension initialization (db, ma)
│   ├── models.py                # All database models
│   └── /blueprints
│       └── /customer
│           ├── __init__.py      # Customer blueprint initialization
│           ├── routes.py        # Customer CRUD routes/controllers
│           └── customerSchemas.py  # Customer Marshmallow schemas
├── app.py                       # Entry point - runs the Flask app
├── config.py                    # Configuration classes for different environments
└── README.md
```

## Key Components

### 1. **config.py** - Multiple Configuration Support
Contains configuration classes for different environments:
- `DevelopmentConfig`: Debug mode enabled, development database
- `TestingConfig`: Testing mode, separate test database
- `ProductionConfig`: Production settings
- `Config`: Base configuration class

**Usage:** Set the `FLASK_CONFIG` environment variable to choose configuration
```bash
set FLASK_CONFIG=development  # Windows
export FLASK_CONFIG=development  # Linux/Mac
```

### 2. **application/extensions.py** - Extension Initialization
Initializes Flask extensions (SQLAlchemy, Marshmallow) without binding to app.
This allows them to be initialized once and bound to the app instance later in the factory.

### 3. **application/__init__.py** - Application Factory (create_app)
The `create_app()` function:
1. Creates a Flask app instance
2. Loads configuration based on environment
3. Initializes extensions (db, ma)
4. Registers blueprints
5. Creates database tables
6. Returns the configured app instance

**Benefits:**
- Multiple app instances for testing
- Different configurations without changing code
- Modular design with blueprints

### 4. **application/models.py** - Database Models
Contains all SQLAlchemy models:
- Customer
- Vehicle
- Mechanic
- Service
- ServiceTicket
- TicketLineItem
- TicketMechanic

### 5. **application/blueprints/** - Modular Route Organization
Each blueprint represents a logical grouping of related routes.

**Customer Blueprint Structure:**
- `__init__.py`: Blueprint registration
- `routes.py`: All customer-related routes (CRUD operations)
- `customerSchemas.py`: Marshmallow schemas for serialization/validation

**Benefits:**
- Separation of concerns
- Easy to maintain and scale
- Can add more blueprints for vehicles, mechanics, services, etc.

### 6. **app.py** - Application Entry Point
Imports `create_app()` and creates the Flask application instance.
This is the file you run to start the server.

## Setting Up the Database

### Before Running:
1. Update `config.py` with your MySQL credentials:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:<YOUR_PASSWORD>@localhost/<YOUR_DATABASE>'
   ```

2. Create the MySQL database (you mentioned you'll do this when ready)

## Running the Application

```bash
# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate

# Run the app
python app.py
```

The server will start on `http://127.0.0.1:5000`

## API Endpoints (Customer)

All customer endpoints are prefixed with `/customers`:

- **POST** `/customers` - Create new customer
- **GET** `/customers` - Get all customers
- **GET** `/customers/<id>` - Get single customer
- **PUT** `/customers/<id>` - Update customer
- **DELETE** `/customers/<id>` - Delete customer

## Advantages of Application Factory Pattern

1. **Modularity**: Code is organized into logical units (blueprints)
2. **Scalability**: Easy to add new features/blueprints without affecting existing code
3. **Multiple Configurations**: Switch between dev, test, and production environments
4. **Testability**: Create isolated app instances for testing
5. **Maintainability**: Clear separation of concerns makes code easier to understand

## Next Steps

You can now extend this pattern by creating additional blueprints for:
- **Vehicles** (`/application/blueprints/vehicle/`)
- **Mechanics** (`/application/blueprints/mechanic/`)
- **Services** (`/application/blueprints/service/`)
- **Service Tickets** (`/application/blueprints/service_ticket/`)

Each blueprint would follow the same structure:
```
/blueprint_name
├── __init__.py          # Blueprint registration
├── routes.py            # CRUD routes
└── schemas.py          # Marshmallow schemas
```

## Environment Variables

- `FLASK_CONFIG`: Set to 'development', 'testing', or 'production'
- `DEV_DATABASE_URL`: Override default development database URL
- `TEST_DATABASE_URL`: Override default testing database URL
- `DATABASE_URL`: Override default production database URL
- `SECRET_KEY`: Set a secure secret key for production

## Notes

- The Pylance type checking warnings you see are informational only and don't affect functionality
- Database tables are automatically created when the app starts (via `db.create_all()`)
- Remember to install required packages: `flask`, `flask-sqlalchemy`, `flask-marshmallow`, `mysql-connector-python`, `marshmallow-sqlalchemy`
