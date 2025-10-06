# Assignment 10 - Inventory Management

## Overview
This assignment adds inventory management functionality to the Mechanic Shop API, allowing tracking of parts used in service tickets.

## Implementation Details

### 1. Database Models

#### Inventory Model
Created a new `Inventory` model in `application/models.py`:
- **id**: Unique identifier (primary key)
- **name**: Part name (String, unique, max 160 chars)
- **price**: Price as float (Numeric 10,2, non-negative)
- **Constraints**: Unique name, non-negative price

#### ServiceInventory Junction Table
Created a many-to-many relationship between ServiceTicket and Inventory:
- **ticket_id**: Foreign key to service_tickets (CASCADE on delete)
- **inventory_id**: Foreign key to inventory (RESTRICT on delete)
- Composite primary key on both fields

#### Updated ServiceTicket Model
Added relationships to support inventory:
- `inventory_assignments`: Direct relationship to ServiceInventory
- `inventory_parts`: View-only relationship to Inventory through junction table

### 2. Inventory Blueprint

#### Structure
```
application/blueprints/inventory/
├── __init__.py          # Blueprint initialization with url_prefix='/inventory'
├── schemas.py           # Marshmallow schema for validation
└── routes.py            # CRUD routes for inventory management
```

#### Schema (schemas.py)
- `InventorySchema`: Uses SQLAlchemyAutoSchema for automatic field mapping
- Validation: name (1-160 chars), price (>= 0)
- Schema instances: `inventory_schema` (single), `inventories_schema` (multiple)

#### Routes (routes.py)

##### Create Inventory Part
- **POST** `/inventory/`
- Rate limited: 10 per hour
- Body: `{ "name": "Oil Filter", "price": 15.99 }`
- Returns: Created inventory part with 201 status

##### List All Inventory
- **GET** `/inventory/`
- Cached for 60 seconds
- Returns: Array of all inventory parts

##### Get Single Inventory Part
- **GET** `/inventory/<inventory_id>`
- Returns: Single inventory part or 404 if not found

##### Update Inventory Part
- **PUT** `/inventory/<inventory_id>`
- Body: Fields to update (e.g., `{ "price": 17.99 }`)
- Returns: Updated inventory part

##### Delete Inventory Part
- **DELETE** `/inventory/<inventory_id>`
- Returns: Success message with 200 status

### 3. Service Ticket Integration

#### Add Part to Ticket
Added route in `application/blueprints/service_tickets/routes.py`:
- **POST** `/service-tickets/<ticket_id>/add-part/<inventory_id>`
- Validates ticket and inventory part existence
- Prevents duplicate additions
- Creates relationship in junction table
- Returns: Success message with part details

### 4. Blueprint Registration

Updated `application/__init__.py`:
- Imported `inventory_bp` from blueprints.inventory
- Registered blueprint with url_prefix='/inventory'

## API Endpoints Summary

### Inventory Endpoints
| Method | Endpoint | Description | Rate Limit | Cache |
|--------|----------|-------------|------------|-------|
| POST | /inventory/ | Create new part | 10/hour | No |
| GET | /inventory/ | List all parts | No | 60s |
| GET | /inventory/<id> | Get single part | No | No |
| PUT | /inventory/<id> | Update part | No | No |
| DELETE | /inventory/<id> | Delete part | No | No |

### Service Ticket Endpoint (New)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /service-tickets/<ticket_id>/add-part/<inventory_id> | Add part to ticket |

## Testing Examples

### 1. Create Inventory Parts
```bash
# Create Oil Filter
curl -X POST http://127.0.0.1:5000/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Oil Filter", "price": 15.99}'

# Create Brake Pads
curl -X POST http://127.0.0.1:5000/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Brake Pads", "price": 45.50}'

# Create Air Filter
curl -X POST http://127.0.0.1:5000/inventory/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Filter", "price": 22.00}'
```

### 2. List All Inventory
```bash
curl http://127.0.0.1:5000/inventory/
```

### 3. Get Single Part
```bash
curl http://127.0.0.1:5000/inventory/1
```

### 4. Update Part Price
```bash
curl -X PUT http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 16.99}'
```

### 5. Add Part to Service Ticket
```bash
# Add Oil Filter (id=1) to Ticket (id=1)
curl -X POST http://127.0.0.1:5000/service-tickets/1/add-part/1
```

### 6. Delete Part
```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

## Database Schema

### inventory Table
```sql
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    name VARCHAR(160) NOT NULL UNIQUE,
    price NUMERIC(10,2) NOT NULL,
    CONSTRAINT ck_inventory_price_nonneg CHECK (price >= 0)
);
```

### service_inventory Junction Table
```sql
CREATE TABLE service_inventory (
    ticket_id INTEGER NOT NULL,
    inventory_id INTEGER NOT NULL,
    PRIMARY KEY (ticket_id, inventory_id),
    FOREIGN KEY (ticket_id) REFERENCES service_tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (inventory_id) REFERENCES inventory(id) ON DELETE RESTRICT
);
```

## Features Implemented

✅ **Inventory Model**: Complete with id, name, and price fields  
✅ **Many-to-Many Relationship**: ServiceTicket ↔ Inventory via junction table  
✅ **Inventory Blueprint**: Organized structure with schemas and routes  
✅ **CRUD Operations**: Full Create, Read, Update, Delete functionality  
✅ **Add Part to Ticket**: Endpoint to associate parts with service tickets  
✅ **Rate Limiting**: Applied to create endpoint (10/hour)  
✅ **Caching**: Applied to list endpoint (60 seconds)  
✅ **Validation**: Schema validation for name and price fields  
✅ **Error Handling**: Proper 404 and 400 responses  
✅ **Database Integration**: Tables created and relationships established  

## Assignment Requirements Checklist

### Inventory Model ✅
- [x] Create Inventory model with id, name, price fields
- [x] Add proper constraints (unique name, non-negative price)

### Many-to-Many Relationship ✅
- [x] Create junction table between Inventory and ServiceTicket
- [x] One ticket can have many parts
- [x] Same part can be used on many tickets
- [x] Update ServiceTicket model with relationships

### Inventory Blueprint ✅
- [x] Create blueprints/inventory folder structure
- [x] Initialize blueprint with url_prefix='/inventory'
- [x] Import routes in __init__.py
- [x] Register blueprint in application/__init__.py
- [x] Create InventorySchema using SQLAlchemyAutoSchema

### Inventory Routes ✅
- [x] POST /inventory/ - Create new part
- [x] GET /inventory/ - List all parts
- [x] GET /inventory/<id> - Get single part
- [x] PUT /inventory/<id> - Update part
- [x] DELETE /inventory/<id> - Delete part

### Service Ticket Integration ✅
- [x] POST /service-tickets/<ticket_id>/add-part/<inventory_id>
- [x] Validate ticket and inventory existence
- [x] Create relationship in junction table
- [x] Return appropriate response

### Testing and Submission ✅
- [x] Database tables created successfully
- [x] All endpoints functional
- [x] Blueprint properly registered
- [x] Ready for Postman testing

## Previous Assignment Features Maintained

All features from previous assignments remain functional:
- Token Authentication (Assignment 7)
- Rate Limiting and Caching (Assignment 6)
- Advanced Queries (Assignment 8)
- Mechanic-Ticket relationships
- Customer authentication and "my-tickets" endpoint
- Pagination on GET Customers route

## Files Modified/Created

### New Files
- `application/blueprints/inventory/__init__.py`
- `application/blueprints/inventory/schemas.py`
- `application/blueprints/inventory/routes.py`
- `README_Assignment10.md`

### Modified Files
- `application/models.py` - Added Inventory and ServiceInventory models
- `application/__init__.py` - Registered inventory blueprint
- `application/blueprints/service_tickets/routes.py` - Added add-part endpoint

## Next Steps

1. **Test in Postman**:
   - Create inventory parts
   - Test all CRUD operations
   - Add parts to service tickets
   - Verify relationships

2. **Create Postman Collection**:
   - Export collection with all requests
   - Include example requests for inventory endpoints
   - Document in collection description

3. **Push to GitHub**:
   - Commit all changes
   - Push to repository
   - Submit GitHub link

## Notes

- The junction table uses a simple two-column approach (ticket_id, inventory_id)
- Optional challenge: Could be extended to include quantity field
- Parts cannot be deleted if they're associated with tickets (RESTRICT constraint)
- Tickets cascade delete their part associations (CASCADE constraint)
- Rate limiting uses in-memory storage (suitable for development)
- Caching reduces database load on frequently accessed endpoints

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Marshmallow**: Schema validation and serialization
- **Flask-Limiter**: Rate limiting
- **Flask-Caching**: Response caching
- **PostgreSQL**: Database (via connection URI)

## Author
Dylan Katina - Assignment 10 Completion

## Date
Assignment completed and ready for testing
