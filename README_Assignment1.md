# Mechanic Shop Database Design – Assignment 1

[![Database](https://img.shields.io/badge/Database-Design-blue?logo=mysql)](https://www.mysql.com/)  
[![ERD](https://img.shields.io/badge/ERD-Entity--Relationship--Diagram-green)](https://dbdiagram.io/d/Mechanic_Shop_ERD-68e2dd0dd2b621e4225b2ce4)  
[![SQL](https://img.shields.io/badge/SQL-Structured--Query--Language-orange)](https://en.wikipedia.org/wiki/SQL)

### 🧱 Assignment Summary
**Objective:** Design and document a normalized relational database schema for a mechanic shop.  
This serves as the foundation for later assignments where the database is implemented, queried, and connected to a Flask API using SQLAlchemy and Marshmallow.

---

### 🧩 Project Overview
In **Lesson 1: Database Design and Planning with ERDs**, the goal was to create an **Entity–Relationship Diagram (ERD)** representing all major entities, attributes, and relationships for a mechanic shop system.

This design captures the relationships between **customers**, **vehicles**, **service tickets**, **mechanics**, and **services**, establishing a scalable relational foundation.

---

### 📂 Folder Structure
```
BE-Mechanic-Shop/
├── Mechanic_Shop_ERD.pdf      ← ERD design document (exported)
├── ERD-SS.png                 ← ERD screenshot for quick reference
├── README_Assignment1.md      ← This file
└── (Next) create_db_tables.py ← Assignment 2 implementation
```

---

### 🧠 Database Design Overview
**Core Entities:**
- **Customers** → individuals who bring vehicles for service
- **Vehicles** → owned by customers; uniquely identified by VIN
- **Service Tickets** → represent maintenance or repair jobs
- **Mechanics** → employees assigned to tickets
- **Services** → catalog of tasks like oil change, tire rotation, brake replacement
- **Ticket Line Items** → individual parts, labor, or service charges per ticket
- **Ticket Mechanics** → many-to-many junction table linking mechanics and tickets

---

### 🧮 Relationships Summary
| Relationship | Type | Description |
|---------------|------|--------------|
| Customers → Vehicles | 1 → ∞ | A customer can have multiple vehicles |
| Vehicles → Service Tickets | 1 → ∞ | Each vehicle can have many tickets |
| Customers → Service Tickets | 1 → ∞ | Customers generate tickets for their vehicles |
| Service Tickets → Mechanics | ∞ → ∞ | Many mechanics can work on many tickets (via TicketMechanics) |
| Service Tickets → Line Items | 1 → ∞ | Each ticket contains multiple charges |
| Services → Line Items | 1 → ∞ | Services can appear on multiple tickets |

---

### 🧾 Deliverables
1. **ERD Diagram** (PDF + Screenshot):
   - [Mechanic_Shop_ERD.pdf](./Mechanic_Shop_ERD.pdf)
   - ![ERD Screenshot](./ERD-SS.png)

2. **Public ERD Link:**  
   [https://dbdiagram.io/d/Mechanic_Shop_ERD-68e2dd0dd2b621e4225b2ce4](https://dbdiagram.io/d/Mechanic_Shop_ERD-68e2dd0dd2b621e4225b2ce4)

---

### 🧩 Tools Used
| Tool | Purpose |
|------|----------|
| **dbdiagram.io** | Create and visualize ERD |
| **MySQL Workbench** | Conceptual design validation |
| **Lucidchart (optional)** | Diagramming alternative |

---

### 🚀 Next Steps
Continue to **Assignment 2 (Lesson 2)** → *Mechanic Shop ORM Models & Database Creation* using **Flask + SQLAlchemy**.

Then progress to **Assignment 3 (Lesson 3)** → *Flask REST API + Marshmallow Schemas* for CRUD endpoints.

---

### 🧾 Credits
**Author:** [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)  
**GitHub:** [growthwithcoding](https://github.com/growthwithcoding)  
**Hashtag:** #growthwithcoding  

Created for **Coding Temple Software Engineering Bootcamp** – Backend Module 1, Lesson 1.
