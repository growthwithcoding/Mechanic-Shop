# Mechanic Shop API - Assignment 4 (Application Factory Pattern)

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?logo=databricks)](https://www.sqlalchemy.org/)
[![Marshmallow](https://img.shields.io/badge/Marshmallow-Schema-green)](https://marshmallow.readthedocs.io/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)](https://www.mysql.com/)
[![Pytest](https://img.shields.io/badge/Testing-Pytest-green?logo=pytest)](https://docs.pytest.org/)

---

## 🧱 Assignment Summary
**Objective:** Refactor the Flask project into the **Application Factory Pattern**, implement full testing, and finalize project configuration for submission.  
The Application Factory Pattern improves modularity, scalability, and testability of the app, supporting multiple configurations (dev/test/prod).

---

## 📂 Final Project Structure
```
BE-Mechanic-Shop/
├── app_factory_runner.py        ← Final Flask runner (renamed from app.py)
├── config.py                    ← Dev/Test/Prod configurations
├── application/
│   ├── __init__.py              ← create_app() + blueprint registration
│   ├── extensions.py            ← db, ma instances (Flask-SQLAlchemy, Marshmallow)
│   ├── models.py                ← SQLAlchemy models
│   └── blueprints/
│       └── customers/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
├── tests_assignment4/
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_customers.py
│   ├── api_smoke_assignment4.rest
│   └── README_Testing_Assignment4.md
├── .env
├── requirements.txt
├── requirements.lock.txt        ← Pinned environment from pip freeze
├── README_Assignment4_Final.md  ← This file
└── run.py                       ← Finalization helper script
```

---

## 🧩 Application Factory Architecture
![Mechanic Shop Application Factory Architecture](./Mechanic_Shop_AppFactory_Architecture.png)

---

## ⚙️ Setup
1. Ensure `.env` exists with your connection string:
   ```bash
   APP_DATABASE_URI=mysql+mysqlconnector://mechanic_user:MySecurePassword123@127.0.0.1/mechanic_shop
   ```

2. Install dependencies (including testing tools):
   ```bash
   pip install -r requirements.txt
   ```

3. Run the finalizer once to rename and freeze:
   ```bash
   python run.py
   ```

---

## 🚀 Run the Application
```bash
python app_factory_runner.py
# Visit: http://127.0.0.1:5000/health
# Visit: http://127.0.0.1:5000/customers
```

---

## 🧪 Testing & Verification
### ✅ Automated Testing (pytest)
Run from project root:
```bash
pytest -q tests_assignment4
```
**All tests pass successfully.**
```
2 passed in 0.62s ✓
```

### ✅ Manual API Testing (REST Client)
Use VS Code REST Client:
```bash
python app_factory_runner.py
```
Then open `tests_assignment4/api_smoke_assignment4.rest` and click **Send Request** on each block.

---

## 🧾 Submission Checklist
- [x] Application Factory Pattern implemented and functional  
- [x] Flask app runs (`python app_factory_runner.py`)  
- [x] Pip freeze snapshot created (`requirements.lock.txt`)  
- [x] All automated tests passing (`pytest -q tests_assignment4`)  
- [x] REST client file verified manually  
- [x] Repository ready for Google Classroom submission  

---

## 🧭 Next Steps
Move on to **Assignment 5 (Lesson 5)** → Continuous Integration, Deployment, and GitHub Actions.

---

## 🧾 Credits
**Author:** [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)  
**GitHub:** [growthwithcoding](https://github.com/growthwithcoding)  
**Hashtag:** #growthwithcoding  

Created for **Coding Temple Software Engineering Bootcamp** – Backend Module 1, Lesson 4.
