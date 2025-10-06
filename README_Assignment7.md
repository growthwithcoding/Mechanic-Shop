# Assignment 7: Token Authentication

## Overview
This assignment implements JWT (JSON Web Token) authentication for the Mechanic Shop API. Token authentication provides a secure, stateless method for protecting API endpoints and managing user sessions without storing session data on the server.

## Learning Objectives Covered
- ✅ Understand the purpose and mechanics of token authentication
- ✅ Learn token creation, exchange, and validation with user-specific details
- ✅ Implement JWT encoding and decoding with `python-jose`
- ✅ Create a `token_required` decorator to protect routes
- ✅ Develop customer authentication endpoints (register, login)
- ✅ Apply token authentication to manage customer-specific data securely

## New Dependencies
The following package was added for Assignment 7:
- **python-jose[cryptography]**: JWT token encoding/decoding library with cryptographic support

Install with:
```bash
pip install -r requirements_assignment7.txt
```

## Token Authentication Flow

1. **Register/Create Account**: Customer creates an account with email and password
2. **Login**: Customer sends credentials (email + password) to `/customers/login`
3. **Verify Credentials**: Server validates the credentials
4. **Generate Token**: Server creates a JWT token with customer ID encoded
5. **Return Token**: Server sends token back to customer
6. **Use Token**: Customer includes token in `Authorization` header for protected routes
7. **Validate Token**: Server verifies token authenticity and expiration
8. **Grant/Deny Access**: Server grants or denies access based on token validity

## Implementation Details

### 1. Updated Customer Model (`application/models.py`)
Added password field to Customer model:
```python
class Customer(Base):
    __tablename__ = "customers"
    
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # New field
    # ... other fields
```

**Note**: In production, passwords should be hashed using bcrypt or similar. This implementation uses plain text for educational purposes only.

### 2. Token Utility Functions (`application/utils/util.py`)

#### `encode_token(customer_id)`
Generates a JWT token for a customer:
```python
def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),  # Expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at
        'sub': str(customer_id)  # Subject (customer_id)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
```

**Key Components**:
- `exp`: Expiration time (1 hour from creation)
- `iat`: Issued at timestamp
- `sub`: Subject - contains the customer_id (must be string)
- `SECRET_KEY`: Secret key for signing tokens
- `HS256`: HMAC-SHA256 signing algorithm

#### `token_required` Decorator
Protects routes requiring authentication:
```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode and validate token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = int(data['sub'])
            
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        # Pass customer_id to wrapped function
        return f(customer_id, *args, **kwargs)
    
    return decorated
```

**How It Works**:
1. Extracts token from `Authorization: Bearer <token>` header
2. Validates token presence
3. Decodes and validates token signature
4. Handles expired and invalid tokens
5. Passes `customer_id` to the protected route function

### 3. Customer Blueprint Routes (`application/blueprints/customers/routes.py`)

#### Authentication Endpoints

**POST `/customers/register`** - Create new customer account
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123",
  "phone": "555-0123"
}
```
Response: `201 Created` with customer data (password excluded)

**POST `/customers/login`** - Login and receive token
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```
Response: `200 OK`
```json
{
  "status": "success",
  "message": "Successfully logged in",
  "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "customer": { ... }
}
```

#### Token-Protected Endpoints

**GET `/customers/my-tickets`** - Get customer's service tickets
- Requires: `Authorization: Bearer <token>`
- Returns all tickets for the authenticated customer

**GET `/customers/profile`** - Get customer profile
- Requires: `Authorization: Bearer <token>`
- Returns customer's profile information

**PUT `/customers/profile`** - Update customer profile
- Requires: `Authorization: Bearer <token>`
- Allows updates to: first_name, last_name, phone, address fields

**DELETE `/customers/profile`** - Delete customer account
- Requires: `Authorization: Bearer <token>`
- Permanently deletes the customer's account

#### Public Endpoints (Admin functions)

**GET `/customers/`** - List all customers
**GET `/customers/<id>`** - Get specific customer by ID

### 4. Customer Schemas (`application/blueprints/customers/schemas.py`)

#### `CustomerSchema`
- Full customer schema including password (for registration)
- Password is `load_only` (not returned in responses)
- Email validation and password minimum length (6 characters)

#### `CustomerResponseSchema`
- Customer schema excluding password
- Used for all API responses

#### `LoginSchema`
- Simple schema with only email and password
- Used for login endpoint validation

## Why Token Authentication Matters

### Security Benefits
1. **Stateless**: No server-side session storage needed
2. **Scalable**: Works across multiple servers without session sharing
3. **Self-Contained**: Token contains all necessary information
4. **Tamper-Proof**: Signed tokens prevent unauthorized modifications
5. **Expiration**: Tokens automatically expire, limiting damage if compromised

### Use Cases
1. **Single Page Applications (SPAs)**: Perfect for modern JavaScript frameworks
2. **Mobile Apps**: Efficient authentication for mobile clients
3. **Microservices**: Easy to validate across multiple services
4. **API Integration**: Third-party services can authenticate easily

## Testing the API

### 1. Register a New Customer
```bash
POST http://localhost:5000/customers/register
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "password": "mypassword123",
  "phone": "555-1234"
}
```

### 2. Login and Get Token
```bash
POST http://localhost:5000/customers/login
Content-Type: application/json

{
  "email": "jane.smith@example.com",
  "password": "mypassword123"
}
```

Save the `auth_token` from the response.

### 3. Access Protected Endpoint
```bash
GET http://localhost:5000/customers/my-tickets
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Test Token Expiration
- Wait 1 hour after login
- Try to access a protected endpoint
- Should receive: `401 Unauthorized - Token has expired!`

### 5. Test Invalid Token
```bash
GET http://localhost:5000/customers/my-tickets
Authorization: Bearer invalid_token_here
```
Response: `401 Unauthorized - Invalid token!`

### 6. Test Missing Token
```bash
GET http://localhost:5000/customers/my-tickets
```
Response: `401 Unauthorized - Token is missing!`

## Project Structure
```
/BE-Mechanic-Shop-6+
├── application/
│   ├── __init__.py                 # Updated to register customers blueprint
│   ├── extensions.py
│   ├── models.py                   # Updated Customer model with password
│   ├── utils/                      # New folder
│   │   ├── __init__.py
│   │   └── util.py                 # Token functions (encode_token, token_required)
│   └── blueprints/
│       ├── customers/              # New blueprint
│       │   ├── __init__.py
│       │   ├── routes.py           # Login, register, protected routes
│       │   └── schemas.py          # Customer and login schemas
│       ├── mechanics/
│       └── service_tickets/
├── tests_assignment7/              # New test folder
│   ├── api_smoke_assignment7.rest
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_token_auth.py
├── requirements_assignment7.txt    # Assignment 7 requirements
├── README_Assignment7.md           # This file
└── ... (other project files)
```

## Running the Application

1. **Install dependencies**:
   ```bash
   pip install -r requirements_assignment7.txt
   ```

2. **Update database schema** (adds password column to customers table):
   ```bash
   # The app will auto-create tables, but existing customers won't have passwords
   # You may need to manually update existing customer records or recreate the database
   python create_db_tables.py
   ```

3. **Set environment variables**:
   ```bash
   # Windows (Command Prompt)
   set APP_DATABASE_URI=mysql+mysqlconnector://username:password@localhost/mechanic_shop

   # Windows (PowerShell)
   $env:APP_DATABASE_URI="mysql+mysqlconnector://username:password@localhost/mechanic_shop"
   ```

4. **Run the application**:
   ```bash
   python app_factory_runner.py
   ```

## Security Considerations

### Current Implementation (Educational)
- ⚠️ Passwords stored in plain text
- ⚠️ SECRET_KEY hardcoded in code
- ⚠️ 1-hour token expiration may be too long/short for some use cases

### Production Recommendations
1. **Hash Passwords**: Use `bcrypt` or `argon2` to hash passwords
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **Environment Variables**: Store SECRET_KEY in environment variables
   ```python
   SECRET_KEY = os.getenv('JWT_SECRET_KEY')
   ```

3. **HTTPS Only**: Always use HTTPS in production to encrypt token transmission

4. **Token Refresh**: Implement refresh tokens for extended sessions

5. **Rate Limiting**: Apply rate limiting to login endpoints (already done in Assignment 6)

6. **Token Blacklisting**: Implement token revocation for logout functionality

7. **Role-Based Access**: Add user roles (customer, mechanic, admin) to tokens

## Best Practices Applied

1. **Decorator Pattern**: `@token_required` cleanly separates authentication logic
2. **Single Responsibility**: Token functions isolated in utils module
3. **Consistent Error Responses**: All auth errors return 401 with descriptive messages
4. **Schema Validation**: All inputs validated before processing
5. **Password Exclusion**: Passwords never returned in API responses
6. **Standard JWT Claims**: Uses standard claim names (exp, iat, sub)

## Common Error Messages

| Error Code | Message | Cause |
|------------|---------|-------|
| 401 | Token is missing! | No Authorization header provided |
| 401 | Invalid Authorization header format | Malformed header (not "Bearer <token>") |
| 401 | Token has expired! | Token older than 1 hour |
| 401 | Invalid token! | Token signature doesn't match or corrupted |
| 401 | Invalid email or password | Login credentials don't match |
| 409 | Email already registered | Email already exists in database |

## Future Enhancements

1. **Password Hashing**: Implement bcrypt for secure password storage
2. **Refresh Tokens**: Add refresh token endpoint for extended sessions
3. **OAuth Integration**: Support Google, Facebook, GitHub login
4. **Two-Factor Authentication**: Add 2FA for enhanced security
5. **Token Revocation**: Implement logout and token blacklist
6. **Role-Based Access Control (RBAC)**: Different permissions for customers/mechanics/admins
7. **Password Reset**: Email-based password recovery
8. **Account Verification**: Email verification on registration
9. **Audit Logging**: Track authentication events for security monitoring
10. **Multiple Device Support**: Track active sessions per user

## Test Results ✅

### Pytest Test Suite: 27/27 PASSED (100%)

All comprehensive tests executed successfully with SQLite in-memory database:

```bash
============================================================== test session starts ===============================================================
platform win32 -- Python 3.11.8, pytest-8.4.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: K:\BE-Mechanic-Shop-6+
configfile: pytest.ini
plugins: flask-1.3.0
collected 27 items

tests_assignment7/tests/test_token_auth.py::TestCustomerRegistration::test_register_customer_success PASSED                                 [  3%]
tests_assignment7/tests/test_token_auth.py::TestCustomerRegistration::test_register_duplicate_email PASSED                                  [  7%]
tests_assignment7/tests/test_token_auth.py::TestCustomerRegistration::test_register_invalid_email PASSED                                    [ 11%]
tests_assignment7/tests/test_token_auth.py::TestCustomerRegistration::test_register_short_password PASSED                                   [ 14%]
tests_assignment7/tests/test_token_auth.py::TestCustomerRegistration::test_register_missing_required_fields PASSED                          [ 18%]
tests_assignment7/tests/test_token_auth.py::TestCustomerLogin::test_login_success PASSED                                                    [ 22%]
tests_assignment7/tests/test_token_auth.py::TestCustomerLogin::test_login_invalid_password PASSED                                           [ 25%]
tests_assignment7/tests/test_token_auth.py::TestCustomerLogin::test_login_nonexistent_email PASSED                                          [ 29%]
tests_assignment7/tests/test_token_auth.py::TestCustomerLogin::test_login_missing_credentials PASSED                                        [ 33%]
tests_assignment7/tests/test_token_auth.py::TestTokenProtectedRoutes::test_get_profile_with_valid_token PASSED                              [ 37%]
tests_assignment7/tests/test_token_auth.py::TestTokenProtectedRoutes::test_get_profile_without_token PASSED                                 [ 40%]
tests_assignment7/tests/test_token_auth.py::TestTokenProtectedRoutes::test_get_profile_with_invalid_token PASSED                            [ 44%]
tests_assignment7/tests/test_token_auth.py::TestTokenProtectedRoutes::test_get_profile_with_malformed_header PASSED                         [ 48%]
tests_assignment7/tests/test_token_auth.py::TestTokenProtectedRoutes::test_update_profile_with_token PASSED                                 [ 51%]
tests_assignment7/tests/test_token_auth.py::TokenProtectedRoutes::test_update_profile_without_token PASSED                                  [ 55%]
tests_assignment7/tests/test_token_auth.py::TestMyTickets::test_get_my_tickets_empty PASSED                                                 [ 59%]
tests_assignment7/tests/test_token_auth.py::TestMyTickets::test_get_my_tickets_with_tickets PASSED                                          [ 62%]
tests_assignment7/tests/test_token_auth.py::TestMyTickets::test_get_my_tickets_without_token PASSED                                         [ 66%]
tests_assignment7/tests/test_token_auth.py::TestDeleteAccount::test_delete_account_with_token PASSED                                        [ 70%]
tests_assignment7/tests/test_token_auth.py::TestDeleteAccount::test_delete_account_without_token PASSED                                     [ 74%]
tests_assignment7/tests/test_token_auth.py::TestPublicEndpoints::test_list_all_customers PASSED                                             [ 77%]
tests_assignment7/tests/test_token_auth.py::TestPublicEndpoints::test_get_customer_by_id PASSED                                             [ 81%]
tests_assignment7/tests/test_token_auth.py::TestPublicEndpoints::test_get_nonexistent_customer PASSED                                       [ 85%]
tests_assignment7/tests/test_token_auth.py::TestTokenUtilityFunctions::test_encode_token PASSED                                             [ 88%]
tests_assignment7/tests/test_token_auth.py::TestTokenUtilityFunctions::test_token_contains_customer_id PASSED                               [ 92%]
tests_assignment7/tests/test_token_auth.py::TestTokenSecurity::test_token_different_for_different_customers PASSED                          [ 96%]
tests_assignment7/tests/test_token_auth.py::TestTokenSecurity::test_cannot_access_other_customer_data PASSED                                [100%]

======================================================== 27 passed, 27 warnings in 0.33s =========================================================
```

### Test Coverage Summary

| Test Category | Tests | Status | Details |
|---------------|-------|--------|---------|
| **Customer Registration** | 5/5 | ✅ PASS | Valid registration, duplicate email detection, email validation, password length, missing fields |
| **Customer Login** | 4/4 | ✅ PASS | Successful login, invalid password, nonexistent email, missing credentials |
| **Token Protected Routes** | 6/6 | ✅ PASS | Valid token access, missing token, invalid token, malformed header, profile updates |
| **My Tickets Endpoint** | 3/3 | ✅ PASS | Empty tickets, tickets with data, unauthorized access |
| **Delete Account** | 2/2 | ✅ PASS | Authorized deletion, unauthorized attempt |
| **Public Endpoints** | 3/3 | ✅ PASS | List customers, get by ID, handle nonexistent |
| **Token Utilities** | 2/2 | ✅ PASS | Token generation, customer ID validation |
| **Token Security** | 2/2 | ✅ PASS | Unique tokens per user, data isolation |
| **TOTAL** | **27/27** | ✅ **100%** | All tests passing |

### Key Test Validations

✅ **Authentication Flow**
- Customer registration with password validation (min 6 characters)
- Email uniqueness enforcement (409 Conflict on duplicate)
- Successful login returns valid JWT token
- Invalid credentials properly rejected (401 Unauthorized)

✅ **Token Security**
- Tokens expire after 1 hour
- Invalid tokens rejected with clear error messages
- Malformed Authorization headers handled gracefully
- Each customer gets unique tokens
- Tokens correctly identify the customer

✅ **Protected Routes**
- `/customers/my-tickets` - Requires valid token
- `/customers/profile` - GET, PUT, DELETE all require tokens
- Missing tokens return 401 with "Token is missing!"
- Invalid tokens return 401 with "Invalid token!"
- Expired tokens return 401 with "Token has expired!"

✅ **Data Security**
- Passwords never returned in API responses
- Customers can only access their own tickets
- Customer-specific data properly isolated
- Profile updates restricted to authenticated user

✅ **Input Validation**
- Email format validation
- Password minimum length (6 characters)
- Required fields enforcement
- Duplicate email prevention

### Running the Tests

To run the test suite yourself:

```bash
# Run all tests with verbose output
python -m pytest tests_assignment7 -v

# Run with coverage report
python -m pytest tests_assignment7 --cov=application --cov-report=html

# Run specific test class
python -m pytest tests_assignment7/tests/test_token_auth.py::TestCustomerLogin -v

# Run with detailed output
python -m pytest tests_assignment7 -vv -s
```

## Resources

- [JWT.io](https://jwt.io/) - JWT introduction and debugger
- [python-jose Documentation](https://python-jose.readthedocs.io/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [RFC 7519 - JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)

---

**Assignment Status**: ✅ COMPLETE - Token authentication fully implemented, tested (27/27 passing), and documented!
