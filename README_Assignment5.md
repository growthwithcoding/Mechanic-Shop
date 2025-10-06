# Assignment 5 – Flask Application Factory + Blueprints

[![Flask](https://img.shields.io/badge/Flask-Application%20Factory-000?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)](https://docs.sqlalchemy.org/)
[![Marshmallow](https://img.shields.io/badge/Marshmallow-Schemas-4DB6AC)](https://marshmallow.readthedocs.io/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC)](https://docs.pytest.org/)

## 🎯 Goal
Refactor the project to the **Application Factory** pattern and add **Blueprints** for:
- `mechanics` (full CRUD)
- `service_tickets` (create, list, assign/remove mechanics)

## 📁 Resulting Structure (key parts)
```
BE-Mechanic-Shop/
├── application/
│   ├── __init__.py            # create_app(), register blueprints
│   ├── extensions.py          # db, ma
│   ├── models.py              # SQLAlchemy models
│   └── blueprints/
│       ├── customers/         # (from A4)
│       ├── mechanics/
│       │   ├── __init__.py    # mechanics_bp = Blueprint(...)
│       │   ├── schemas.py     # MechanicSchema
│       │   └── routes.py      # CRUD
│       └── service_tickets/
│           ├── __init__.py    # service_tickets_bp = Blueprint(...)
│           ├── schemas.py     # ServiceTicketSchema
│           └── routes.py      # create/list/assign/remove
├── app_factory_runner.py      # run server via create_app()
├── tests_assignment5/
│   ├── api_smoke_assignment5.rest
│   └── tests/
│       ├── conftest.py
│       ├── test_mechanics_crud.py
│       └── test_service_tickets.py
├── requirements.txt
└── requirements_assignment5.txt
```

## 🔧 Endpoints
**Mechanics** (prefix `/mechanics`):
- `POST /` – create mechanic
- `GET /` – list mechanics
- `GET /<id>` – get one
- `PUT /<id>` – update
- `DELETE /<id>` – delete

**Service Tickets** (prefix `/service-tickets`):
- `POST /` – create ticket
- `GET /` – list tickets
- `PUT /<ticket_id>/assign-mechanic/<mechanic_id>` – assign mechanic
- `PUT /<ticket_id>/remove-mechanic/<mechanic_id>` – remove mechanic

## ✅ How to Run
```bash
# 1) install
(venv) pip install -r requirements.txt

# 2) run server (uses create_app())
(venv) python app_factory_runner.py

# 3) tests (optional)
(venv) pytest tests_assignment5 -q

# 4) manual smoke (VS Code REST Client)
# open: tests_assignment5/api_smoke_assignment5.rest
```
> Ensure your `.env` has `APP_DATABASE_URI` set to your MySQL DSN.

## 🧪 Notes
- Tests seed a minimal customer/vehicle as needed.
- Blueprints are registered inside `create_app()` with URL prefixes:
  - `/mechanics`
  - `/service-tickets`

## 👤 Author
**Austin Carlson** — [GitHub: growthwithcoding](https://github.com/growthwithcoding) · [LinkedIn](https://www.linkedin.com/in/austin-carlson-720b65375/)  
#growthwithcoding
