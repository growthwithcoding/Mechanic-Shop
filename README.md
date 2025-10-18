# Mechanic Shop SQLAlchemy Models

This project implements SQLAlchemy models based on the Mechanic Shop ERD, following the assignment requirements.

## Setup Instructions

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

**Windows:**
```bash
pip install flask flask-sqlalchemy mysql-connector-python
```

**Mac/Linux:**
```bash
pip3 install flask flask-sqlalchemy mysql-connector-python
```

### 4. Create Database in MySQL Workbench

Open MySQL Workbench and create a new database:

```sql
CREATE DATABASE mechanic_shop;
```

### 5. Configure Database Connection

Open `app.py` and update line 11 with your MySQL credentials:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/mechanic_shop'
```

Replace:
- `YOUR_PASSWORD` with your MySQL root password
- `mechanic_shop` with your database name (if different)

### 6. Run the Application

```bash
python app.py
```

The application will:
1. Create all database tables based on the models
2. Print "Database tables created successfully!"
3. Start the Flask development server

## Models Implemented

### 1. Customer
- **Primary Key:** customer_id
- **Relationships:**
  - One-to-Many with Vehicle
  - One-to-Many with ServiceTicket

### 2. Vehicle
- **Primary Key:** vehicle_id
- **Foreign Keys:** customer_id
- **Relationships:**
  - Many-to-One with Customer
  - One-to-Many with ServiceTicket

### 3. Mechanic
- **Primary Key:** mechanic_id
- **Relationships:**
  - One-to-Many with TicketMechanic (junction table)

### 4. Service
- **Primary Key:** service_id
- **Relationships:**
  - One-to-Many with TicketLineItem

### 5. ServiceTicket
- **Primary Key:** ticket_id
- **Foreign Keys:** vehicle_id, customer_id
- **Relationships:**
  - Many-to-One with Vehicle
  - Many-to-One with Customer
  - One-to-Many with TicketLineItem
  - One-to-Many with TicketMechanic (junction table)

### 6. TicketLineItem
- **Primary Key:** line_item_id
- **Foreign Keys:** ticket_id, service_id
- **Relationships:**
  - Many-to-One with ServiceTicket
  - Many-to-One with Service

### 7. TicketMechanic (Junction Table)
- **Composite Primary Key:** ticket_id, mechanic_id
- **Foreign Keys:** ticket_id, mechanic_id
- **Relationships:**
  - Many-to-One with ServiceTicket
  - Many-to-One with Mechanic
- **Purpose:** Enables Many-to-Many relationship between ServiceTicket and Mechanic

## Relationship Types Implemented

### One-to-Many Relationships:
1. **Customer → Vehicles:** A customer can own multiple vehicles
2. **Customer → ServiceTickets:** A customer can have multiple service tickets
3. **Vehicle → ServiceTickets:** A vehicle can have multiple service tickets
4. **ServiceTicket → TicketLineItems:** A service ticket can have multiple line items
5. **Service → TicketLineItems:** A service can appear in multiple ticket line items

### Many-to-Many Relationship:
1. **ServiceTicket ↔ Mechanic:** Through the `ticket_mechanics` junction table
   - A service ticket can have multiple mechanics working on it
   - A mechanic can work on multiple service tickets
   - The junction table stores additional data: role and minutes_worked

## Key Features

- ✅ All tables match the ERD exactly
- ✅ Foreign key constraints properly defined
- ✅ Bidirectional relationships using `back_populates`
- ✅ Proper data types mapped to MySQL types
- ✅ Nullable constraints applied appropriately
- ✅ Unique constraints on email fields and VIN
- ✅ Composite primary key on junction table
- ✅ Default values for timestamps and boolean fields

## Database Schema

The models will create the following tables:
- customers
- vehicles
- mechanics
- services
- service_tickets
- ticket_line_items
- ticket_mechanics

All relationships and constraints from the ERD are preserved in the database schema.
