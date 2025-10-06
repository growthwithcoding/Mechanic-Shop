# Assignment 8: Advanced Queries Utilizing SQLAlchemy Relationships

## Overview
This assignment focuses on leveraging SQLAlchemy relationships to create advanced query endpoints. By treating relationships as Python lists, we can use built-in list operations (`.append()`, `.remove()`, `.sort()`, etc.) to manipulate data and create insightful API endpoints. We also implement query parameters and pagination for efficient data retrieval.

## Learning Objectives Covered
- ✅ Recap one-to-many and many-to-many relationships in SQLAlchemy
- ✅ Access related data using SQLAlchemy relationship attributes as Python lists
- ✅ Modify many-to-many relationships by appending and removing items
- ✅ Implement custom sorting using `.sort()` with lambda functions
- ✅ Incorporate query parameters into API endpoints for filtering and searching
- ✅ Apply pagination techniques (limit and offset) for efficient data retrieval

## New Dependencies
No new dependencies required for Assignment 8. This assignment builds on existing SQLAlchemy relationships.

## Key Concepts

### SQLAlchemy Relationships as Python Lists

When you query an object with relationships, SQLAlchemy provides access to related objects as Python lists:

```python
# One-to-Many: Customer -> ServiceTickets
customer = db.session.get(Customer, 1)
customer_tickets = customer.tickets  # Returns List[ServiceTicket]
print(len(customer_tickets))  # Number of tickets

# Many-to-Many: ServiceTicket <-> Mechanics
ticket = db.session.get(ServiceTicket, 1)
assigned_mechanics = ticket.mechanics  # Returns List[Mechanic]
ticket.mechanics.append(new_mechanic)  # Add mechanic
ticket.mechanics.remove(old_mechanic)  # Remove mechanic
```

### Lambda Functions for Sorting

Lambda functions provide a concise way to define sorting keys:

```python
# Basic lambda syntax
add = lambda x, y: x + y
print(add(3, 4))  # Output: 7

# Sorting with lambda
words = ['apple', 'banana', 'pear', 'kiwi']
words.sort(key=lambda word: len(word))
print(words)  # Output: ['pear', 'kiwi', 'apple', 'banana']

# Sorting mechanics by ticket count (descending)
mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
```

### Query Parameters

Query parameters allow passing data via URL without a JSON payload:

```
# Basic query parameter
GET /books?title=python

# Multiple query parameters
GET /books?limit=10&offset=20

# Pagination
GET /customers?page=2&per_page=10
```

### Pagination

Pagination divides large datasets into manageable chunks:

- **limit**: Maximum number of results to return
- **offset**: Number of results to skip
- **page**: Page number (alternative to offset)
- **per_page**: Results per page (alternative to limit)

## Implementation Details

### 1. Edit Service Ticket Mechanics (PUT `/service-tickets/<int:ticket_id>/edit`)

This endpoint allows bulk addition and removal of mechanics from a ticket.

**Endpoint**: `PUT /service-tickets/<int:ticket_id>/edit`

**Request Body**:
```json
{
  "add_ids": [1, 2, 3],
  "remove_ids": [4, 5]
}
```

**Implementation** (`application/blueprints/service_tickets/routes.py`):
```python
@service_tickets_bp.put("/<int:ticket_id>/edit")
def edit_ticket_mechanics(ticket_id: int):
    """
    Bulk add/remove mechanics from a ticket.
    Accepts add_ids and remove_ids arrays in request body.
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, HTTPStatus.NOT_FOUND
    
    payload = request.get_json() or {}
    add_ids = payload.get('add_ids', [])
    remove_ids = payload.get('remove_ids', [])
    
    # Remove mechanics
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
    
    # Add mechanics
    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
    
    db.session.commit()
    
    return {
        "message": f"Ticket {ticket_id} mechanics updated",
        "mechanics": [m.mechanic_id for m in ticket.mechanics]
    }, HTTPStatus.OK
```

**Key Features**:
- Accepts arrays of mechanic IDs to add and remove
- Prevents duplicate additions (checks if mechanic already assigned)
- Safely handles removal (checks if mechanic is assigned)
- Returns updated list of mechanic IDs
- Uses `.append()` and `.remove()` on the relationship list

**Response Example**:
```json
{
  "message": "Ticket 1 mechanics updated",
  "mechanics": [1, 2, 3]
}
```

### 2. Most Active Mechanics (GET `/mechanics/most-active`)

This endpoint returns mechanics sorted by the number of tickets they've worked on.

**Endpoint**: `GET /mechanics/most-active`

**Implementation** (`application/blueprints/mechanics/routes.py`):
```python
@mechanics_bp.get("/most-active")
def get_most_active_mechanics():
    """
    Returns mechanics sorted by number of tickets worked (descending).
    Uses lambda function to sort by length of tickets relationship.
    """
    mechanics = db.session.scalars(db.select(Mechanic)).all()
    
    # Sort mechanics by ticket count (descending)
    mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
    
    # Create response with ticket counts
    result = [
        {
            "mechanic_id": m.mechanic_id,
            "full_name": m.full_name,
            "email": m.email,
            "tickets_worked": len(m.tickets),
            "is_active": m.is_active
        }
        for m in mechanics
    ]
    
    return jsonify(result), HTTPStatus.OK
```

**Key Features**:
- Uses `.sort()` with lambda function to sort by ticket count
- `reverse=True` for descending order (most active first)
- Includes ticket count in response for transparency
- Leverages the many-to-many relationship `mechanic.tickets`

**Response Example**:
```json
[
  {
    "mechanic_id": 3,
    "full_name": "John Smith",
    "email": "john@example.com",
    "tickets_worked": 15,
    "is_active": true
  },
  {
    "mechanic_id": 1,
    "full_name": "Jane Doe",
    "email": "jane@example.com",
    "tickets_worked": 12,
    "is_active": true
  }
]
```

### 3. Paginated Customers (GET `/customers/`)

This endpoint adds pagination to the customer list endpoint.

**Endpoint**: `GET /customers/?page=1&per_page=10`

**Query Parameters**:
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Results per page (default: 10, max: 100)

**Implementation** (`application/blueprints/customers/routes.py`):
```python
@customers_bp.get("/")
@cache.cached(timeout=60, query_string=True)  # Cache varies by query params
def list_customers():
    """
    List all customers with pagination support.
    Query params: page (default 1), per_page (default 10, max 100)
    """
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Validate parameters
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10
    
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Query with limit and offset
    customers = db.session.scalars(
        db.select(Customer)
        .order_by(Customer.customer_id)
        .limit(per_page)
        .offset(offset)
    ).all()
    
    # Get total count for metadata
    total_count = db.session.scalar(
        db.select(db.func.count(Customer.customer_id))
    )
    
    # Calculate total pages
    total_pages = (total_count + per_page - 1) // per_page
    
    return jsonify({
        "customers": customers_response_schema.dump(customers, many=True),
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }), HTTPStatus.OK
```

**Key Features**:
- Default pagination: page 1, 10 items per page
- Maximum per_page: 100 (prevents excessive data requests)
- Returns pagination metadata (total count, total pages, navigation flags)
- Uses SQLAlchemy `.limit()` and `.offset()` for efficient queries
- Cache varies by query string (different cache for each page)

**Response Example**:
```json
{
  "customers": [
    {
      "customer_id": 11,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "555-0123"
    }
    // ... 9 more customers
  ],
  "pagination": {
    "page": 2,
    "per_page": 10,
    "total_count": 45,
    "total_pages": 5,
    "has_next": true,
    "has_prev": true
  }
}
```

## Relationship Overview

### Current Model Relationships

```python
# One-to-Many: Customer -> Vehicles
class Customer(Base):
    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="customer")
    tickets: Mapped[List["ServiceTicket"]] = relationship(back_populates="customer")

# One-to-Many: Customer -> ServiceTickets
class ServiceTicket(Base):
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
    customer: Mapped["Customer"] = relationship(back_populates="tickets")

# Many-to-Many: ServiceTicket <-> Mechanics (via ticket_mechanics)
class ServiceTicket(Base):
    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary="ticket_mechanics", 
        back_populates="tickets", 
        viewonly=True
    )

class Mechanic(Base):
    tickets: Mapped[List["ServiceTicket"]] = relationship(
        secondary="ticket_mechanics", 
        back_populates="mechanics", 
        viewonly=True
    )

# Junction Table: ticket_mechanics
class TicketMechanic(Base):
    __tablename__ = "ticket_mechanics"
    
    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.ticket_id"), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanics.mechanic_id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(16), default="ASSIST")
    minutes_worked: Mapped[int] = mapped_column(Integer, default=0)
```

## Testing the API

### 1. Edit Ticket Mechanics

**Add mechanics 1, 2, 3 and remove mechanic 4 from ticket 1**:
```http
PUT http://localhost:5000/service-tickets/1/edit
Content-Type: application/json

{
  "add_ids": [1, 2, 3],
  "remove_ids": [4]
}
```

**Expected Response**:
```json
{
  "message": "Ticket 1 mechanics updated",
  "mechanics": [1, 2, 3]
}
```

### 2. Get Most Active Mechanics

```http
GET http://localhost:5000/mechanics/most-active
```

**Expected Response**:
```json
[
  {
    "mechanic_id": 2,
    "full_name": "Alice Johnson",
    "email": "alice@shop.com",
    "tickets_worked": 8,
    "is_active": true
  },
  {
    "mechanic_id": 1,
    "full_name": "Bob Smith",
    "email": "bob@shop.com",
    "tickets_worked": 5,
    "is_active": true
  }
]
```

### 3. Paginated Customers

**First page (default)**:
```http
GET http://localhost:5000/customers/
```

**Specific page and size**:
```http
GET http://localhost:5000/customers/?page=2&per_page=5
```

**Expected Response**:
```json
{
  "customers": [ /* 5 customers */ ],
  "pagination": {
    "page": 2,
    "per_page": 5,
    "total_count": 23,
    "total_pages": 5,
    "has_next": true,
    "has_prev": true
  }
}
```

## Benefits of This Approach

### 1. Treating Relationships as Lists
- **Intuitive**: Uses familiar Python list operations
- **Flexible**: Easy to add, remove, count, or iterate
- **Powerful**: Can leverage all list methods (`.sort()`, `.filter()`, etc.)

### 2. Lambda Functions for Sorting
- **Concise**: One-line sorting logic
- **Flexible**: Can sort by any attribute or calculation
- **Readable**: Clear intent when properly formatted

### 3. Query Parameters
- **User-Friendly**: Parameters visible in URL
- **Cacheable**: GET requests can be cached
- **RESTful**: Follows REST best practices

### 4. Pagination
- **Performance**: Reduces database load and response size
- **UX**: Manageable data chunks for users
- **Scalability**: Handles large datasets efficiently

## Common Use Cases

### Relationship Manipulation

```python
# Add mechanic to multiple tickets
for ticket_id in [1, 2, 3]:
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, 5)
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
db.session.commit()

# Find tickets without mechanics
tickets = db.session.scalars(db.select(ServiceTicket)).all()
unassigned = [t for t in tickets if len(t.mechanics) == 0]

# Count customer's total tickets
customer = db.session.get(Customer, 1)
ticket_count = len(customer.tickets)
```

### Advanced Sorting

```python
# Sort by multiple criteria
mechanics.sort(key=lambda m: (len(m.tickets), m.full_name), reverse=True)

# Sort by calculated value
tickets.sort(key=lambda t: len(t.line_items) * 100, reverse=True)

# Sort by relationship attribute
customers.sort(key=lambda c: len(c.vehicles))
```

### Query Parameters

```python
# Search query
search_term = request.args.get('search', '')
title_filter = f"%{search_term}%"
results = db.session.scalars(
    db.select(Book).where(Book.title.like(title_filter))
).all()

# Filtering
status = request.args.get('status', 'OPEN')
tickets = db.session.scalars(
    db.select(ServiceTicket).where(ServiceTicket.status == status)
).all()
```

## Best Practices

### 1. Relationship Manipulation
- Always check if item exists before appending
- Always check if item is in list before removing
- Commit changes after bulk operations
- Handle database errors gracefully

### 2. Sorting
- Use lambda functions for simple sorting keys
- Consider performance for large datasets
- Sort in Python for small datasets, SQL for large ones
- Use `reverse=True` for descending order

### 3. Pagination
- Always validate page numbers (min: 1)
- Set maximum per_page limit (e.g., 100)
- Return pagination metadata
- Use offset = (page - 1) * per_page
- Cache with query_string=True for query parameter caching

### 4. Query Parameters
- Provide sensible defaults
- Validate all user inputs
- Document parameter options
- Use type conversion (e.g., `type=int`)

## Project Structure

```
/BE-Mechanic-Shop-6+
├── application/
│   ├── blueprints/
│   │   ├── customers/
│   │   │   └── routes.py          # ✨ Updated: Pagination
│   │   ├── mechanics/
│   │   │   └── routes.py          # ✨ New: most-active endpoint
│   │   └── service_tickets/
│   │       └── routes.py          # ✨ New: edit endpoint
│   └── models.py                  # Existing relationships
├── requirements_assignment8.txt   # Assignment 8 requirements (same as 7)
├── requirements.txt               # Updated to Assignment 8
└── README_Assignment8.md          # This file
```

## Performance Considerations

### When to Sort in Python vs SQL

**Sort in Python (after query)**:
- Small datasets (< 1000 records)
- Complex sorting logic not expressible in SQL
- Need to sort by calculated Python values

**Sort in SQL (in query)**:
```python
# Better for large datasets
mechanics = db.session.scalars(
    db.select(Mechanic)
    .order_by(db.func.count(TicketMechanic.mechanic_id).desc())
    .group_by(Mechanic.mechanic_id)
).all()
```

### Pagination Best Practices

**Good**:
```python
# Efficient - only loads what's needed
query.limit(10).offset(20)
```

**Bad**:
```python
# Inefficient - loads all, then slices
all_records = query.all()
page_records = all_records[20:30]
```

### Caching with Pagination

```python
@cache.cached(timeout=60, query_string=True)
def list_items():
    # Cache varies by query parameters
    # /items?page=1 has different cache than /items?page=2
    pass
```

## Extending the Implementation

### Optional Enhancements

1. **Search by Name**:
```python
@mechanics_bp.get("/most-active")
def get_most_active():
    search = request.args.get('search', '')
    mechanics = db.session.scalars(db.select(Mechanic)).all()
    
    if search:
        mechanics = [m for m in mechanics if search.lower() in m.full_name.lower()]
    
    mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
    return jsonify([...]), HTTPStatus.OK
```

2. **Limit Results**:
```python
@mechanics_bp.get("/most-active")
def get_most_active():
    limit = request.args.get('limit', 10, type=int)
    mechanics = db.session.scalars(db.select(Mechanic)).all()
    mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
    
    return jsonify([...])[:limit], HTTPStatus.OK
```

3. **Filter by Active Status**:
```python
@mechanics_bp.get("/most-active")
def get_most_active():
    active_only = request.args.get('active_only', 'true') == 'true'
    mechanics = db.session.scalars(db.select(Mechanic)).all()
    
    if active_only:
        mechanics = [m for m in mechanics if m.is_active]
    
    mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
    return jsonify([...]), HTTPStatus.OK
```

## Common Errors and Solutions

### Error: "list.remove(x): x not in list"
```python
# Problem
ticket.mechanics.remove(mechanic)

# Solution
if mechanic in ticket.mechanics:
    ticket.mechanics.remove(mechanic)
```

### Error: Duplicate entries in many-to-many
```python
# Problem
ticket.mechanics.append(mechanic)  # Adds even if already exists

# Solution
if mechanic not in ticket.mechanics:
    ticket.mechanics.append(mechanic)
```

### Error: Invalid page number
```python
# Problem
page = request.args.get('page', type=int)  # Could be None or negative

# Solution
page = request.args.get('page', 1, type=int)
if page < 1:
    page = 1
```

## Resources

- [SQLAlchemy Relationships Documentation](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [Python Lambda Functions](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions)
- [Flask Request Arguments](https://flask.palletsprojects.com/en/latest/api/#flask.Request.args)
- [REST API Pagination Best Practices](https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/)

## Summary

Assignment 8 demonstrates the power of SQLAlchemy relationships by treating them as Python lists. This approach enables:

✅ **Easy Manipulation**: Add/remove items using familiar list operations  
✅ **Insightful Queries**: Sort and analyze data using lambda functions  
✅ **Efficient Retrieval**: Implement pagination for large datasets  
✅ **Flexible Filtering**: Use query parameters for dynamic requests  

By leveraging these techniques, you can create powerful, efficient, and user-friendly APIs that scale well with growing data.

---

**Assignment Status**: ✅ READY FOR IMPLEMENTATION
