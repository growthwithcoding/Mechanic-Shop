# Mechanic Shop API - Assignment 5

[![Flask](https://img.shields.io/badge/Flask-Application%20Factory-000?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)](https://docs.sqlalchemy.org/)
[![Marshmallow](https://img.shields.io/badge/Marshmallow-Schemas-4DB6AC)](https://marshmallow.readthedocs.io/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC)](https://docs.pytest.org/)
[![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?logo=postman)](https://www.postman.com/)

## 🎯 Project Overview

A comprehensive RESTful API for managing a mechanic shop's operations, built with Flask using the **Application Factory** pattern and **Blueprints** architecture. This project demonstrates professional API development practices including:

- Modular blueprint-based architecture
- Complete CRUD operations for mechanics
- Service ticket management with mechanic assignments
- Automated test suite with pytest
- Postman collection with automated tests
- SQLAlchemy ORM with MySQL database

## 📁 Project Structure

```
BE-Mechanic-Shop/
├── application/
│   ├── __init__.py                    # create_app(), register blueprints
│   ├── extensions.py                  # db, ma instances
│   ├── models.py                      # SQLAlchemy models
│   └── blueprints/
│       ├── mechanics/
│       │   ├── __init__.py           # mechanics_bp = Blueprint(...)
│       │   ├── schemas.py            # MechanicSchema
│       │   └── routes.py             # CRUD endpoints
│       └── service_tickets/
│           ├── __init__.py           # service_tickets_bp = Blueprint(...)
│           ├── schemas.py            # ServiceTicketSchema
│           └── routes.py             # ticket management endpoints
├── tests_assignment5/
│   ├── api_smoke_assignment5.rest    # VS Code REST Client tests
│   └── tests/
│       ├── conftest.py               # pytest fixtures
│       ├── test_mechanics_crud.py    # mechanics endpoint tests
│       └── test_service_tickets.py   # service tickets tests
├── Assignment5_Create_Postman_Collection.py  # Postman collection generator
├── app_factory_runner.py             # Flask application runner
├── requirements.txt                  # Python dependencies
└── .env                              # Environment variables (DATABASE_URI)
```

## 🔧 API Endpoints

### Health Check
- `GET /health` – API health status

### Mechanics Management (prefix: `/mechanics`)
- `POST /mechanics` – Create a new mechanic
- `GET /mechanics` – List all mechanics
- `GET /mechanics/<id>` – Get mechanic by ID
- `PUT /mechanics/<id>` – Update mechanic
- `DELETE /mechanics/<id>` – Delete mechanic

### Service Tickets (prefix: `/service-tickets`)
- `POST /service-tickets` – Create a new service ticket
- `GET /service-tickets` – List all service tickets
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` – Assign mechanic to ticket
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` – Remove mechanic from ticket

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Postman (optional, for API testing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/growthwithcoding/Mechanic-Shop.git
   cd BE-Mechanic-Shop
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   
   Create a `.env` file in the project root:
   ```env
   APP_DATABASE_URI=mysql+mysqlconnector://username:password@localhost/mechanic_shop
   ```

5. **Create database**
   ```sql
   -- In MySQL Workbench or CLI
   CREATE DATABASE mechanic_shop;
   ```

6. **Run the application**
   ```bash
   python app_factory_runner.py
   ```
   
   The API will be available at `http://127.0.0.1:5000`

## 📮 Postman Collection Generator

### Assignment Submission Tool

For Assignment 5 submission, use the included **Postman Collection Generator** to create a comprehensive API test collection.

#### Generate Postman Collection

Run the generator script:
```bash
python Assignment5_Create_Postman_Collection.py
```

This will create:
- `Mechanic_Shop_API_Collection.postman_collection.json`

#### What's Included

The generated Postman collection contains:

✅ **10 Pre-configured API Requests** organized in folders:
- Health Check (1 endpoint)
- Mechanics CRUD (5 endpoints)
- Service Tickets (4 endpoints)

✅ **Automated Tests** for each endpoint:
- Status code validation
- Response structure verification
- Data validation
- Automatic variable capture (mechanic_id, ticket_id)

✅ **Collection Variables**:
- `base_url` - API server URL (http://127.0.0.1:5000)
- `mechanic_id` - Auto-captured from Create Mechanic response
- `ticket_id` - Auto-captured from Create Ticket response

#### Using the Collection

1. **Generate the collection file**:
   ```bash
   python Assignment5_Create_Postman_Collection.py
   ```

2. **Import into Postman**:
   - Open Postman
   - Click "Import" button
   - Select `Mechanic_Shop_API_Collection.postman_collection.json`

3. **Start your API server**:
   ```bash
   python app_factory_runner.py
   ```

4. **Run the collection**:
   - In Postman, click "Run collection"
   - Watch automated tests validate all endpoints
   - View detailed test results

#### Collection Features

- **Smart Variable Management**: IDs are automatically captured from POST responses and used in subsequent requests
- **Comprehensive Tests**: Each request includes multiple test assertions
- **Sample Data**: Pre-filled request bodies with realistic test data
- **Organized Structure**: Requests grouped by functionality
- **Ready for Submission**: Perfect for demonstrating API functionality

## 🧪 Testing

### Automated Tests (pytest)

Run the test suite:
```bash
# Run all tests
pytest tests_assignment5 -v

# Run with coverage
pytest tests_assignment5 --cov=application

# Run specific test file
pytest tests_assignment5/tests/test_mechanics_crud.py -v
```

### Manual Testing (VS Code REST Client)

1. Install the "REST Client" extension in VS Code
2. Open `tests_assignment5/api_smoke_assignment5.rest`
3. Click "Send Request" above each endpoint

## 📊 Database Schema

The application uses the following main tables:
- `customers` - Customer information
- `vehicles` - Vehicle details linked to customers
- `mechanics` - Mechanic profiles and salary information
- `service_tickets` - Service work orders
- `ticket_mechanics` - Many-to-many relationship between tickets and mechanics
- `services` - Service catalog
- `ticket_line_items` - Individual items on service tickets

## 🏗️ Architecture Highlights

### Application Factory Pattern
The app uses Flask's application factory pattern for better testability and configuration management:
```python
from application import create_app
app = create_app()
```

### Blueprints
Modular route organization using Flask blueprints:
- Each feature has its own blueprint
- Routes are prefixed at registration
- Easy to add new features without cluttering main app

### Extensions
Shared extensions initialized once and used across blueprints:
- SQLAlchemy (`db`)
- Marshmallow (`ma`)

## 🔐 Environment Variables

Required environment variables in `.env`:
```env
APP_DATABASE_URI=mysql+mysqlconnector://user:password@host/database
```

Optional:
```env
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📝 Assignment Notes

### What's New in Assignment 5
- ✅ Refactored to Application Factory pattern
- ✅ Implemented Blueprint architecture
- ✅ Full CRUD for Mechanics
- ✅ Service Ticket creation and listing
- ✅ Mechanic assignment/removal from tickets
- ✅ Comprehensive pytest test suite
- ✅ **NEW**: Postman collection generator for submission

### For Grading/Submission
1. Ensure all tests pass: `pytest tests_assignment5 -v`
2. Generate Postman collection: `python Assignment5_Create_Postman_Collection.py`
3. Submit the generated JSON file along with your code
4. Document any additional features in comments

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Verify MySQL is running
mysql -u root -p

# Check .env file exists and has correct credentials
cat .env
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Kill process on port 5000 (macOS/Linux)
lsof -ti:5000 | xargs kill -9
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Marshmallow Schemas](https://marshmallow.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Postman Learning Center](https://learning.postman.com/)

## 👤 Author

**Austin Carlson**
- GitHub: [@growthwithcoding](https://github.com/growthwithcoding)
- LinkedIn: [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)

#growthwithcoding

## 📄 License

This project is part of Coding Temple's Backend Development course.

---

**Happy Coding! 🚀**
