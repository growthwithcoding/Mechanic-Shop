# Assignment 9: Utilizing Junction Tables with Additional Fields

## Overview
This assignment explores the implementation of junction tables with additional fields in many-to-many relationships. We learn when to use a simple `db.Table` versus creating a full model for the junction table, and understand how to store metadata and additional attributes in the relationship itself.

## Learning Objectives Covered
- ✅ Understand the purpose of junction tables in many-to-many relationships
- ✅ Differentiate between `db.Table` for simple junctions and model-based junctions
- ✅ Explore pros and cons of each approach
- ✅ Implement a model-based junction table with additional fields
- ✅ Store and manage metadata in the junction table

## Key Concepts

### What is a Junction Table?

A **junction table** (also called an association table or join table) is a table that connects two entities in a many-to-many relationship. For example:

- **Many mechanics** can work on **many service tickets**
- **Many service tickets** can have **many mechanics**

The junction table stores the connections between these two entities.

### Two Approaches to Junction Tables

#### 1. Simple Junction Table (`db.Table`)

Use `db.Table` when the junction table only needs to store the foreign keys with no additional data.

**Example Structure**:
```
mechanic_service_ticket
├── mechanic_id (FK → mechanics.id)
└── ticket_id (FK → service_tickets.id)
```

**When to Use**:
- ✅ Pure many-to-many relationship
- ✅ No metadata needed
- ✅ Simple linking only

**Pros**:
- Simple and concise
- Less code to maintain
- Automatic relationship management

**Cons**:
- ❌ Cannot store additional information
- ❌ No direct access to junction records
- ❌ Limited querying capabilities

**Code Example**:
```python
# Simple junction table using db.Table
mechanic_service_ticket = db.Table(
    'mechanic_service_ticket',
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.ticket_id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.mechanic_id"))
)

class Mechanic(Base):
    __tablename__ = "mechanics"
    
    mechanic_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    
    # Simple many-to-many using secondary
    tickets: Mapped[List["ServiceTicket"]] = relationship(
        secondary=mechanic_service_ticket,
        back_populates="mechanics"
    )

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    
    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    problem_description: Mapped[str] = mapped_column(Text)
    
    # Simple many-to-many using secondary
    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary=mechanic_service_ticket,
        back_populates="tickets"
    )
```

#### 2. Model-Based Junction Table (Full Model Class)

Use a full model when the junction table needs to store additional information beyond just the foreign keys.

**Example Structure**:
```
ticket_mechanics
├── ticket_id (FK → service_tickets.ticket_id) [PK]
├── mechanic_id (FK → mechanics.mechanic_id) [PK]
├── role (e.g., "LEAD" or "ASSIST")
└── minutes_worked (tracking time spent)
```

**When to Use**:
- ✅ Need to store metadata (dates, quantities, status, etc.)
- ✅ Need direct access to junction records
- ✅ Complex business logic in the relationship
- ✅ Need to query the junction table independently

**Pros**:
- Stores additional data and metadata
- Full model capabilities (validation, methods, etc.)
- Can query junction records directly
- More control over the relationship

**Cons**:
- ❌ More complex to implement
- ❌ Requires explicit relationship management
- ❌ More code to maintain

## Our Implementation: TicketMechanic Junction Table

In our Mechanic Shop application, we use a **model-based junction table** called `TicketMechanic` to connect `ServiceTicket` and `Mechanic` entities with additional metadata.

### Why a Model-Based Junction Table?

We need to track:
1. **Role**: Is the mechanic a "LEAD" or "ASSIST" on this ticket?
2. **Minutes Worked**: How much time did the mechanic spend on this ticket?

This metadata is essential for:
- Payroll calculations
- Performance tracking
- Workload distribution
- Billing accuracy

### Complete Implementation

#### Junction Table Model (`application/models.py`)

```python
class TicketMechanic(Base):
    """
    Junction table connecting ServiceTickets and Mechanics
    with additional fields for role and time tracking.
    """
    __tablename__ = "ticket_mechanics"
    __table_args__ = (
        CheckConstraint("minutes_worked >= 0", name="ck_tm_minutes_nonneg"),
        CheckConstraint("role in ('LEAD','ASSIST')", name="ck_tm_role"),
    )

    # Composite Primary Key (ticket_id + mechanic_id)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("service_tickets.ticket_id", ondelete="CASCADE"),
        primary_key=True
    )
    mechanic_id: Mapped[int] = mapped_column(
        ForeignKey("mechanics.mechanic_id", ondelete="RESTRICT"),
        primary_key=True
    )
    
    # Additional Fields (the reason we need a full model!)
    role: Mapped[str] = mapped_column(String(16), default="ASSIST", nullable=False)
    minutes_worked: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships to parent entities
    ticket: Mapped["ServiceTicket"] = relationship(back_populates="assignments")
    mechanic: Mapped["Mechanic"] = relationship(back_populates="assignments")
```

#### Mechanic Model

```python
class Mechanic(Base):
    __tablename__ = "mechanics"
    
    mechanic_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(40))
    salary_cents: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Direct access to junction records
    assignments: Mapped[List["TicketMechanic"]] = relationship(
        back_populates="mechanic",
        cascade="all, delete-orphan"
    )
    
    # Convenient many-to-many access (viewonly - read-only)
    tickets: Mapped[List["ServiceTicket"]] = relationship(
        secondary="ticket_mechanics",
        back_populates="mechanics",
        viewonly=True  # Read-only, use assignments to modify
    )
```

#### ServiceTicket Model

```python
class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    
    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.vehicle_id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    problem_description: Mapped[Optional[str]] = mapped_column(Text)

    # Direct access to junction records
    assignments: Mapped[List["TicketMechanic"]] = relationship(
        back_populates="ticket",
        cascade="all, delete-orphan"
    )
    
    # Convenient many-to-many access (viewonly - read-only)
    mechanics: Mapped[List["Mechanic"]] = relationship(
        secondary="ticket_mechanics",
        back_populates="tickets",
        viewonly=True  # Read-only, use assignments to modify
    )
```

### Key Implementation Details

#### 1. Composite Primary Key

```python
ticket_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
mechanic_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
```

- Both columns form the primary key
- Ensures each mechanic-ticket pair is unique
- No separate `id` column needed

#### 2. Cascade Deletion

```python
ForeignKey("service_tickets.ticket_id", ondelete="CASCADE")
ForeignKey("mechanics.mechanic_id", ondelete="RESTRICT")
```

- **CASCADE**: When a ticket is deleted, remove all mechanic assignments
- **RESTRICT**: Prevent mechanic deletion if they have ticket assignments

#### 3. Check Constraints

```python
CheckConstraint("minutes_worked >= 0", name="ck_tm_minutes_nonneg")
CheckConstraint("role in ('LEAD','ASSIST')", name="ck_tm_role")
```

- Ensures `minutes_worked` is never negative
- Restricts `role` to valid values only

#### 4. Dual Relationship Pattern

Each parent model has TWO relationships:

**Direct Access** (`assignments`):
- Full access to junction records
- Can read/write all fields (`role`, `minutes_worked`)
- Use for modifications

**Convenience Access** (`tickets`/`mechanics`):
- Quick access to related entities
- Read-only (`viewonly=True`)
- Use for simple queries

## Working with Junction Tables

### Creating Assignments

#### Method 1: Using Junction Records Directly

```python
from application.models import ServiceTicket, Mechanic, TicketMechanic

# Get entities
ticket = db.session.get(ServiceTicket, 1)
mechanic = db.session.get(Mechanic, 5)

# Create assignment with additional fields
assignment = TicketMechanic(
    ticket_id=ticket.ticket_id,
    mechanic_id=mechanic.mechanic_id,
    role="LEAD",
    minutes_worked=120
)

db.session.add(assignment)
db.session.commit()
```

#### Method 2: Using Relationships

```python
# Create assignment and add to ticket
assignment = TicketMechanic(
    mechanic_id=5,
    role="LEAD",
    minutes_worked=120
)

ticket.assignments.append(assignment)
db.session.commit()
```

### Querying Junction Data

#### Get All Assignments for a Ticket

```python
ticket = db.session.get(ServiceTicket, 1)

# Access all assignments with full details
for assignment in ticket.assignments:
    print(f"Mechanic: {assignment.mechanic.full_name}")
    print(f"Role: {assignment.role}")
    print(f"Minutes: {assignment.minutes_worked}")
```

#### Get All Mechanics for a Ticket (Simple)

```python
ticket = db.session.get(ServiceTicket, 1)

# Quick access to mechanics (no junction data)
for mechanic in ticket.mechanics:
    print(f"Mechanic: {mechanic.full_name}")
```

#### Query Junction Table Directly

```python
# Find all LEAD assignments
leads = db.session.scalars(
    db.select(TicketMechanic).where(TicketMechanic.role == "LEAD")
).all()

# Find assignments with significant time
long_jobs = db.session.scalars(
    db.select(TicketMechanic).where(TicketMechanic.minutes_worked > 300)
).all()

# Get total minutes for a mechanic
mechanic_id = 5
total_minutes = db.session.scalar(
    db.select(db.func.sum(TicketMechanic.minutes_worked))
    .where(TicketMechanic.mechanic_id == mechanic_id)
)
```

### Updating Junction Data

```python
# Update an existing assignment
assignment = db.session.get(TicketMechanic, (ticket_id, mechanic_id))
assignment.minutes_worked += 60  # Add 1 hour
assignment.role = "LEAD"  # Promote to lead

db.session.commit()
```

### Removing Assignments

```python
# Remove specific assignment
ticket = db.session.get(ServiceTicket, 1)
mechanic = db.session.get(Mechanic, 5)

# Find and remove the assignment
assignment = db.session.get(TicketMechanic, (ticket.ticket_id, mechanic.mechanic_id))
if assignment:
    db.session.delete(assignment)
    db.session.commit()
```

## API Implementation Examples

### Create Assignment Endpoint

```python
@service_tickets_bp.post("/<int:ticket_id>/assign-mechanic")
def assign_mechanic(ticket_id: int):
    """
    Assign a mechanic to a ticket with role and initial minutes.
    """
    payload = request.get_json()
    mechanic_id = payload.get('mechanic_id')
    role = payload.get('role', 'ASSIST')
    minutes_worked = payload.get('minutes_worked', 0)
    
    # Validate entities exist
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not ticket or not mechanic:
        return {"error": "Ticket or mechanic not found"}, 404
    
    # Check if assignment already exists
    existing = db.session.get(TicketMechanic, (ticket_id, mechanic_id))
    if existing:
        return {"error": "Mechanic already assigned to this ticket"}, 409
    
    # Create assignment
    assignment = TicketMechanic(
        ticket_id=ticket_id,
        mechanic_id=mechanic_id,
        role=role,
        minutes_worked=minutes_worked
    )
    
    db.session.add(assignment)
    db.session.commit()
    
    return {
        "message": "Mechanic assigned successfully",
        "assignment": {
            "ticket_id": ticket_id,
            "mechanic_id": mechanic_id,
            "mechanic_name": mechanic.full_name,
            "role": role,
            "minutes_worked": minutes_worked
        }
    }, 201
```

### Get Ticket Assignments Endpoint

```python
@service_tickets_bp.get("/<int:ticket_id>/assignments")
def get_ticket_assignments(ticket_id: int):
    """
    Get all mechanic assignments for a ticket with details.
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}, 404
    
    assignments_data = [
        {
            "mechanic_id": assignment.mechanic_id,
            "mechanic_name": assignment.mechanic.full_name,
            "role": assignment.role,
            "minutes_worked": assignment.minutes_worked,
            "hours_worked": assignment.minutes_worked / 60
        }
        for assignment in ticket.assignments
    ]
    
    return jsonify({
        "ticket_id": ticket_id,
        "total_assignments": len(assignments_data),
        "total_hours": sum(a["hours_worked"] for a in assignments_data),
        "assignments": assignments_data
    }), 200
```

### Update Assignment Endpoint

```python
@service_tickets_bp.put("/<int:ticket_id>/assignments/<int:mechanic_id>")
def update_assignment(ticket_id: int, mechanic_id: int):
    """
    Update role or minutes for an existing assignment.
    """
    assignment = db.session.get(TicketMechanic, (ticket_id, mechanic_id))
    if not assignment:
        return {"error": "Assignment not found"}, 404
    
    payload = request.get_json()
    
    if 'role' in payload:
        if payload['role'] not in ['LEAD', 'ASSIST']:
            return {"error": "Invalid role. Must be LEAD or ASSIST"}, 400
        assignment.role = payload['role']
    
    if 'minutes_worked' in payload:
        if payload['minutes_worked'] < 0:
            return {"error": "Minutes worked cannot be negative"}, 400
        assignment.minutes_worked = payload['minutes_worked']
    
    db.session.commit()
    
    return {
        "message": "Assignment updated successfully",
        "assignment": {
            "ticket_id": ticket_id,
            "mechanic_id": mechanic_id,
            "role": assignment.role,
            "minutes_worked": assignment.minutes_worked
        }
    }, 200
```

## Real-World Use Cases

### 1. Payroll Calculations

```python
def calculate_mechanic_pay(mechanic_id: int, period_start: date, period_end: date):
    """
    Calculate total pay for a mechanic based on hours worked.
    """
    mechanic = db.session.get(Mechanic, mechanic_id)
    hourly_rate = mechanic.salary_cents / 100 / 2080  # Annual to hourly
    
    # Get all assignments in period
    assignments = db.session.scalars(
        db.select(TicketMechanic)
        .join(ServiceTicket)
        .where(
            TicketMechanic.mechanic_id == mechanic_id,
            ServiceTicket.opened_at.between(period_start, period_end)
        )
    ).all()
    
    total_minutes = sum(a.minutes_worked for a in assignments)
    total_hours = total_minutes / 60
    total_pay = total_hours * hourly_rate
    
    return {
        "mechanic_id": mechanic_id,
        "mechanic_name": mechanic.full_name,
        "period_start": period_start,
        "period_end": period_end,
        "total_hours": total_hours,
        "hourly_rate": hourly_rate,
        "total_pay": total_pay
    }
```

### 2. Lead Mechanic Report

```python
def get_lead_mechanics_report():
    """
    Get all lead mechanics and their tickets.
    """
    lead_assignments = db.session.scalars(
        db.select(TicketMechanic).where(TicketMechanic.role == "LEAD")
    ).all()
    
    report = {}
    for assignment in lead_assignments:
        mechanic_name = assignment.mechanic.full_name
        if mechanic_name not in report:
            report[mechanic_name] = []
        
        report[mechanic_name].append({
            "ticket_id": assignment.ticket_id,
            "description": assignment.ticket.problem_description,
            "hours_worked": assignment.minutes_worked / 60
        })
    
    return report
```

### 3. Workload Distribution

```python
def get_mechanic_workload():
    """
    Analyze workload distribution across mechanics.
    """
    mechanics = db.session.scalars(db.select(Mechanic)).all()
    
    workload = []
    for mechanic in mechanics:
        total_minutes = sum(a.minutes_worked for a in mechanic.assignments)
        active_tickets = sum(
            1 for a in mechanic.assignments 
            if a.ticket.status in ['OPEN', 'IN_PROGRESS']
        )
        
        workload.append({
            "mechanic_id": mechanic.mechanic_id,
            "mechanic_name": mechanic.full_name,
            "total_hours": total_minutes / 60,
            "active_tickets": active_tickets,
            "lead_count": sum(1 for a in mechanic.assignments if a.role == "LEAD")
        })
    
    # Sort by total hours (busiest first)
    workload.sort(key=lambda x: x['total_hours'], reverse=True)
    
    return workload
```

## Comparison: db.Table vs Model

### Example Scenario: Library Books and Authors

#### Using db.Table (Simple)

```python
# No additional data needed - just link books and authors
book_authors = db.Table(
    'book_authors',
    Base.metadata,
    db.Column('book_id', db.ForeignKey('books.book_id')),
    db.Column('author_id', db.ForeignKey('authors.author_id'))
)

class Book(Base):
    __tablename__ = "books"
    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    
    authors: Mapped[List["Author"]] = relationship(
        secondary=book_authors,
        back_populates="books"
    )

class Author(Base):
    __tablename__ = "authors"
    author_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    
    books: Mapped[List["Book"]] = relationship(
        secondary=book_authors,
        back_populates="authors"
    )
```

#### Using Model (Complex)

```python
# Need to track author's contribution type and page range
class BookAuthor(Base):
    __tablename__ = "book_authors"
    
    book_id: Mapped[int] = mapped_column(ForeignKey('books.book_id'), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.author_id'), primary_key=True)
    
    # Additional fields
    contribution_type: Mapped[str] = mapped_column(String(50))  # "primary", "co-author", "editor"
    chapter_start: Mapped[Optional[int]] = mapped_column(Integer)
    chapter_end: Mapped[Optional[int]] = mapped_column(Integer)
    
    book: Mapped["Book"] = relationship(back_populates="authorships")
    author: Mapped["Author"] = relationship(back_populates="authorships")

class Book(Base):
    __tablename__ = "books"
    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    
    authorships: Mapped[List["BookAuthor"]] = relationship(back_populates="book")
    authors: Mapped[List["Author"]] = relationship(
        secondary="book_authors",
        back_populates="books",
        viewonly=True
    )

class Author(Base):
    __tablename__ = "authors"
    author_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    
    authorships: Mapped[List["BookAuthor"]] = relationship(back_populates="author")
    books: Mapped[List["Book"]] = relationship(
        secondary="book_authors",
        back_populates="authors",
        viewonly=True
    )
```

## Decision Matrix: When to Use Each Approach

| Criteria | db.Table | Model-Based Junction |
|----------|----------|---------------------|
| Additional fields needed? | ❌ No | ✅ Yes |
| Need to query junction directly? | ❌ No | ✅ Yes |
| Business logic on relationship? | ❌ No | ✅ Yes |
| Simple linking only? | ✅ Yes | ❌ Overkill |
| Need validation on junction data? | ❌ No | ✅ Yes |
| Timestamps or metadata? | ❌ No | ✅ Yes |
| Code complexity tolerance | ✅ Low | ⚠️ Medium |

## Best Practices

### 1. Composite Primary Keys

```python
# DO: Use composite primary key for junction tables
ticket_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
mechanic_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)

# DON'T: Add unnecessary surrogate key
# id: Mapped[int] = mapped_column(primary_key=True)  # Not needed!
```

### 2. Cascade Settings

```python
# Think about what should happen when parent is deleted
ForeignKey("service_tickets.ticket_id", ondelete="CASCADE")  # Delete assignments
ForeignKey("mechanics.mechanic_id", ondelete="RESTRICT")     # Protect mechanics
```

### 3. Validation with Check Constraints

```python
# Add database-level validation
__table_args__ = (
    CheckConstraint("minutes_worked >= 0", name="ck_minutes_nonneg"),
    CheckConstraint("role in ('LEAD','ASSIST')", name="ck_valid_role"),
)
```

### 4. Default Values

```python
# Provide sensible defaults
role: Mapped[str] = mapped_column(String(16), default="ASSIST")
minutes_worked: Mapped[int] = mapped_column(Integer, default=0)
```

### 5. Dual Relationship Pattern

```python
# Provide both direct and convenient access
class Mechanic(Base):
    # Direct access to junction (read/write)
    assignments: Mapped[List["TicketMechanic"]] = relationship(...)
    
    # Convenient access to related entities (read-only)
    tickets: Mapped[List["ServiceTicket"]] = relationship(..., viewonly=True)
```

## Common Patterns

### Pattern 1: Ordered Relationships

```python
class CourseStudent(Base):
    __tablename__ = "course_students"
    
    course_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
    enrollment_date: Mapped[date] = mapped_column(Date)
    grade: Mapped[Optional[str]] = mapped_column(String(2))
    
    # Order students by enrollment date
    __table_args__ = (
        db.Index('ix_enrollment_date', 'course_id', 'enrollment_date'),
    )
```

### Pattern 2: Quantity Tracking

```python
class OrderItem(Base):
    __tablename__ = "order_items"
    
    order_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price_cents: Mapped[int] = mapped_column(Integer)
    
    @property
    def total_price_cents(self):
        """Calculate line item total."""
        return self.quantity * self.unit_price_cents
```

### Pattern 3: Status Tracking

```python
class ProjectMember(Base):
    __tablename__ = "project_members"
    
    project_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(...), primary_key=True)
    role: Mapped[str] = mapped_column(String(20))
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    @property
    def is_active(self):
        """Check if member is currently active."""
        return self.left_at is None
```

## Testing Junction Tables

### Creating Test Data

```python
def test_create_assignment():
    """Test creating a mechanic assignment."""
    # Create entities
    mechanic = Mechanic(full_name="Test Mechanic", email="test@example.com")
    ticket = ServiceTicket(
        vehicle_id=1,
        customer_id=1,
        problem_description="Test issue"
    )
    
    db.session.add_all([mechanic, ticket])
    db.session.flush()  # Get IDs without committing
    
    # Create assignment
    assignment = TicketMechanic(
        ticket_id=ticket.ticket_id,
        mechanic_id=mechanic.mechanic_id,
        role="LEAD",
        minutes_worked=120
    )
    
    db.session.add(assignment)
    db.session.commit()
    
    # Verify
    assert assignment.role == "LEAD"
    assert assignment.minutes_worked == 120
    assert assignment.ticket == ticket
    assert assignment.mechanic == mechanic
```

### Testing Relationships

```python
def test_ticket_assignments():
    """Test accessing assignments through ticket."""
    ticket = db.session.get(ServiceTicket, 1)
    
    # Should have assignments
    assert len(ticket.assignments) > 0
    
    # Each assignment should have mechanic details
    for assignment in ticket.assignments:
        assert assignment.mechanic is not None
        assert assignment.role in ['LEAD', 'ASSIST']
        assert assignment.minutes_worked >= 0
```

### Testing Constraints

```python
def test_negative_minutes_rejected():
    """Test that negative minutes are rejected."""
    from sqlalchemy.exc import IntegrityError
    
    assignment = TicketMechanic(
        ticket_id=1,
        mechanic_id=1,
        minutes_worked=-10  # Invalid!
    )
    
    db.session.add(assignment)
    
    with pytest.raises(IntegrityError):
        db.session.commit()
```

## Migration Considerations

### Converting from db.Table to Model

If you start with `db.Table` and later need to add fields:

1. **Create the new model class**
2. **Create migration to add new columns**
3. **Update relationship definitions**
4. **Test thoroughly**

```python
# Before (db.Table)
mechanic_ticket = db.Table(...)

# After (Model)
class TicketMechanic(Base):
    # Keep same table name!
    __tablename__ = "ticket_mechanics"
    # ... model definition
```

## Performance Tips

### 1. Eager Loading

```python
# Load assignments with mechanics in one query
ticket = db.session.scalars(
    db.select(ServiceTicket)
    .options(db.joinedload(ServiceTicket.assignments).joinedload(TicketMechanic.mechanic))
    .where(ServiceTicket.ticket_id == 1)
).first()

# Now accessing assignments doesn't trigger additional queries
for assignment in ticket.assignments:
    print(assignment.mechanic.full_name)  # No extra query!
```

### 2. Batch Operations

```python
# Create multiple assignments efficiently
assignments = [
    TicketMechanic(ticket_id=1, mechanic_id=m_id, role="ASSIST")
    for m_id in [1, 2, 3, 4, 5]
]

db.session.add_all(assignments)
db.session.commit()  # Single commit for all
```

### 3. Bulk Updates

```python
# Update multiple assignments at once
db.session.execute(
    db.update(TicketMechanic)
    .where(TicketMechanic.ticket_id == 1)
    .values(role="ASSIST")
)
db.session.commit()
```

## Summary

Assignment 9 demonstrates the power and flexibility of model-based junction tables:

✅ **Store Additional Data**: Track metadata like roles, timestamps, quantities  
✅ **Direct Querying**: Query junction table independently  
✅ **Business Logic**: Add validation, constraints, and computed properties  
✅ **Flexibility**: Adapt to complex business requirements  

### Key Takeaways

1. **Use `db.Table`** for simple many-to-many relationships with no additional data
2. **Use a Model** when you need to store metadata or have complex logic
3. **Composite Primary Keys** are sufficient for junction tables (no need for surrogate keys)
4. **Dual Relationships** provide both direct access (assignments) and convenient access (mechanics/tickets)
5. **Check Constraints** add database-level validation for data integrity

### When to Choose Each Approach

**Choose db.Table when:**
- Pure linking with no additional data
- Simple CRUD operations
- Minimizing code complexity

**Choose Model when:**
- Need to store timestamps, quantities, status, etc.
- Need to query the junction table directly
- Complex business rules or validation
- Need computed properties or methods

---

**Assignment Status**: ✅ COMPLETE

Our Mechanic Shop already implements a model-based junction table (`TicketMechanic`) with additional fields (`role` and `minutes_worked`), demonstrating best practices for complex many-to-many relationships!

## Resources

- [SQLAlchemy Many-to-Many Relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many)
- [Association Objects](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object)
- [Composite Primary Keys](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#composite-primary-keys)
- [Check Constraints](https://docs.sqlalchemy.org/en/20/core/constraints.html#check-constraint)

## Project Structure

```
/BE-Mechanic-Shop-6+
├── application/
│   ├── models.py                     # ✅ TicketMechanic junction table implemented
│   └── blueprints/
│       ├── mechanics/
│       │   └── routes.py            # Mechanic endpoints
│       └── service_tickets/
│           └── routes.py            # Service ticket endpoints
├── README_Assignment9.md            # This file
└── requirements.txt                 # Project dependencies
```
