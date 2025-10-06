# Mechanic Shop API – Assignment 3

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?logo=flask)](https://flask.palletsprojects.com/)  
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?logo=databricks)](https://www.sqlalchemy.org/)  
[![Marshmallow](https://img.shields.io/badge/Marshmallow-Schema-green)](https://marshmallow.readthedocs.io/)  
[![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)](https://www.mysql.com/)

### 🧱 Assignment Summary
**Objective:** Build a RESTful API layer on top of your Mechanic Shop database using Flask, with **Marshmallow** for validation & serialization.  
You will implement CRUD endpoints (Create, Read, Update, Delete) for the **Customer** resource.

---

### 📂 Folder Structure
```
BE-Mechanic-Shop/
├── .env
├── create_db_tables.py
├── inspect_db_contents.py
├── app.py                       ← Flask API (Assignment 3)
└── requirements.txt / requirements_assignment3.txt
```

---

### ⚙️ Setup
Install the extra dependencies for this assignment:
```powershell
pip install flask-marshmallow marshmallow-sqlalchemy
```
(Optional) Save a separate requirements snapshot:
```powershell
pip freeze > requirements_assignment3.txt
```

Ensure your `.env` still contains the DB connection (from Assignment 2):
```bash
APP_DATABASE_URI=mysql+mysqlconnector://mechanic_user:MySecurePassword123@127.0.0.1/mechanic_shop
```

---

### 🚀 Run the API
```powershell
python app.py
```
You should see Flask running on `http://127.0.0.1:5000`.

Health check:
```
GET http://127.0.0.1:5000/health
```

---

### 🔌 Endpoints (Customer)
- **GET /customers** – List customers (+ vehicle preview)
- **GET /customers/<id>** – Retrieve a single customer
- **POST /customers** – Create a customer (validated)
- **PUT /customers/<id>** – Update a customer (validated, unique email check)
- **DELETE /customers/<id>** – Delete a customer

#### Example Requests (PowerShell with curl)
Create:
```powershell
curl -X POST http://127.0.0.1:5000/customers `
  -H "Content-Type: application/json" `
  -d '{ "first_name":"Alex","last_name":"Rios","email":"alex.rios@example.com","phone":"555-123-9999" }'
```

List:
```powershell
curl http://127.0.0.1:5000/customers
```

Update:
```powershell
curl -X PUT http://127.0.0.1:5000/customers/1 `
  -H "Content-Type: application/json" `
  -d '{ "first_name":"Casey","last_name":"Ng","email":"casey@example.com","city":"Denver" }'
```

Delete:
```powershell
curl -X DELETE http://127.0.0.1:5000/customers/1
```

---

### 🧠 Notes
- This app **reuses the Flask app and SQLAlchemy session** from `create_db_tables.py`. Importing it does **not** re-seed data because seeding is inside `if __name__ == "__main__":` there.
- Error responses return standard HTTP codes (400/404) with helpful messages.
- The schema uses Marshmallow to validate email and string lengths.
- Vehicle details are included as a simple read-only preview on GETs.

---

### 🧭 Next Steps
- Add Marshmallow schemas for **Vehicle** and **ServiceTicket** and expose CRUD endpoints for them.
- Add a computed ticket total (sum of `quantity * unit_price_cents`) to a ticket serializer.
- Write Postman collection or `.http` file with example API calls.

---

### 🧾 Credits
**Author:** [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)  
**GitHub:** [growthwithcoding](https://github.com/growthwithcoding)  
**Hashtag:** #growthwithcoding  

Created for **Coding Temple Software Engineering Bootcamp** – Backend Module 1, Lesson 3.
