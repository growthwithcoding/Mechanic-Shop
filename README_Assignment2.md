# Mechanic Shop Backend – Lesson 2

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?logo=flask)](https://flask.palletsprojects.com/)  
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?logo=databricks)](https://www.sqlalchemy.org/)  
[![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)](https://www.mysql.com/)

### 🧱 Assignment Summary
**Objective:** Build ORM models and relationships in Flask using SQLAlchemy to bring the ERD from Assignment 1 to life.  
This includes creating the database tables, seeding demo data, and verifying relationships with inspection scripts.

---

### 📂 Folder Structure
```
BE-Mechanic-Shop/
├── venv/
├── .env
├── requirements.txt
├── create_db_tables.py
└── inspect_db_contents.py
```

---

### ⚙️ Environment Setup
1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install flask flask-sqlalchemy mysql-connector-python python-dotenv
   ```

3. Create your database and user in MySQL Workbench:
   ```sql
   CREATE DATABASE mechanic_shop;
   CREATE USER 'mechanic_user'@'127.0.0.1' IDENTIFIED BY 'MySecurePassword123';
   GRANT ALL PRIVILEGES ON mechanic_shop.* TO 'mechanic_user'@'127.0.0.1';
   ```

4. Add this line to your `.env` file:
   ```bash
   APP_DATABASE_URI=mysql+mysqlconnector://mechanic_user:MySecurePassword123@127.0.0.1/mechanic_shop
   ```

---

### 🚀 Running the Project
1. **Create Tables and Seed Data**
   ```powershell
   python create_db_tables.py
   ```
   Expected output:
   ```
   Connecting as: mechanic_user@127.0.0.1
   ✅ Tables created for Mechanic Shop. Using .env connection URI.
   ```

2. **Inspect Data**
   ```powershell
   python inspect_db_contents.py
   ```
   Displays all seeded data and relationship summaries.

---

### 🧩 Files Summary
| File | Purpose |
|------|----------|
| **create_db_tables.py** | Builds tables, defines models, and seeds demo data |
| **inspect_db_contents.py** | Prints record counts and relationships |
| **requirements.txt** | Captures dependencies for reproducibility |

---

### 🚀 Next Steps
Continue to **Assignment 3 (Lesson 3)** → *RESTful APIs, Schemas, and Routing in Flask*.  
This next step introduces **Marshmallow** for schema validation, serialization, and CRUD endpoint creation.

---

### 🧾 Credits
**Author:** [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)  
**GitHub:** [growthwithcoding](https://github.com/growthwithcoding)  
**Hashtag:** #growthwithcoding  

Created for **Coding Temple Software Engineering Bootcamp** – Backend Module 1, Lesson 2.
