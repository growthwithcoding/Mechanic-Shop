# tests_assignment7/tests/test_token_auth.py
import pytest
from application.models import Customer
from application.utils.util import encode_token


class TestCustomerRegistration:
    """Test customer registration endpoint."""
    
    def test_register_customer_success(self, client):
        """Test successful customer registration."""
        response = client.post('/customers/register', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepass123',
            'phone': '555-1234'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Customer registered successfully'
        assert data['customer']['email'] == 'john.doe@example.com'
        assert 'password' not in data['customer']  # Password should not be in response
    
    def test_register_duplicate_email(self, client, test_customer):
        """Test registration with duplicate email."""
        response = client.post('/customers/register', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': test_customer.email,
            'password': 'password123'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert data['message'] == 'Email already registered'
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post('/customers/register', json={
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'not-an-email',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'errors' in data
    
    def test_register_short_password(self, client):
        """Test registration with password too short."""
        response = client.post('/customers/register', json={
            'first_name': 'Alice',
            'last_name': 'Wonder',
            'email': 'alice@example.com',
            'password': 'short'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'errors' in data
    
    def test_register_missing_required_fields(self, client):
        """Test registration with missing required fields."""
        response = client.post('/customers/register', json={
            'email': 'incomplete@example.com'
        })
        
        assert response.status_code == 400


class TestCustomerLogin:
    """Test customer login and token generation."""
    
    def test_login_success(self, client, test_customer):
        """Test successful login returns token."""
        response = client.post('/customers/login', json={
            'email': test_customer.email,
            'password': 'testpass123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['message'] == 'Successfully logged in'
        assert 'auth_token' in data
        assert len(data['auth_token']) > 0
        assert 'customer' in data
        assert 'password' not in data['customer']
    
    def test_login_invalid_password(self, client, test_customer):
        """Test login with incorrect password."""
        response = client.post('/customers/login', json={
            'email': test_customer.email,
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['message'] == 'Invalid email or password'
    
    def test_login_nonexistent_email(self, client):
        """Test login with non-existent email."""
        response = client.post('/customers/login', json={
            'email': 'nonexistent@example.com',
            'password': 'somepassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['message'] == 'Invalid email or password'
    
    def test_login_missing_credentials(self, client):
        """Test login with missing credentials."""
        response = client.post('/customers/login', json={
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400


class TestTokenProtectedRoutes:
    """Test routes that require token authentication."""
    
    def test_get_profile_with_valid_token(self, client, test_customer, auth_token):
        """Test accessing profile with valid token."""
        response = client.get(
            '/customers/profile',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == test_customer.email
        assert 'password' not in data
    
    def test_get_profile_without_token(self, client):
        """Test accessing profile without token."""
        response = client.get('/customers/profile')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['message'] == 'Token is missing!'
    
    def test_get_profile_with_invalid_token(self, client):
        """Test accessing profile with invalid token."""
        response = client.get(
            '/customers/profile',
            headers={'Authorization': 'Bearer invalid_token_123'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['message'] == 'Invalid token!'
    
    def test_get_profile_with_malformed_header(self, client, auth_token):
        """Test accessing profile with malformed Authorization header."""
        response = client.get(
            '/customers/profile',
            headers={'Authorization': auth_token}  # Missing "Bearer" prefix
        )
        
        assert response.status_code == 401
    
    def test_update_profile_with_token(self, client, test_customer, auth_token):
        """Test updating profile with valid token."""
        response = client.put(
            '/customers/profile',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={
                'first_name': 'Updated',
                'phone': '555-9999'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Profile updated successfully'
        assert data['customer']['first_name'] == 'Updated'
        assert data['customer']['phone'] == '555-9999'
    
    def test_update_profile_without_token(self, client):
        """Test updating profile without token."""
        response = client.put(
            '/customers/profile',
            json={'phone': '555-1111'}
        )
        
        assert response.status_code == 401


class TestMyTickets:
    """Test customer-specific ticket retrieval."""
    
    def test_get_my_tickets_empty(self, client, auth_token):
        """Test getting tickets when customer has no tickets."""
        response = client.get(
            '/customers/my-tickets',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['ticket_count'] == 0
        assert data['tickets'] == []
    
    def test_get_my_tickets_with_tickets(self, client, auth_token, test_ticket):
        """Test getting tickets when customer has tickets."""
        response = client.get(
            '/customers/my-tickets',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['ticket_count'] == 1
        assert len(data['tickets']) == 1
        assert data['tickets'][0]['ticket_id'] == test_ticket.ticket_id
    
    def test_get_my_tickets_without_token(self, client):
        """Test getting tickets without authentication."""
        response = client.get('/customers/my-tickets')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['message'] == 'Token is missing!'


class TestDeleteAccount:
    """Test account deletion with token authentication."""
    
    def test_delete_account_with_token(self, client, auth_token, test_customer):
        """Test deleting account with valid token."""
        response = client.delete(
            '/customers/profile',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Successfully deleted account' in data['message']
        
        # Verify customer is actually deleted
        from application.extensions import db
        deleted_customer = db.session.get(Customer, test_customer.customer_id)
        assert deleted_customer is None
    
    def test_delete_account_without_token(self, client):
        """Test deleting account without token."""
        response = client.delete('/customers/profile')
        
        assert response.status_code == 401


class TestPublicEndpoints:
    """Test public customer endpoints (admin functions)."""
    
    def test_list_all_customers(self, client, test_customer):
        """Test listing all customers (no auth required)."""
        response = client.get('/customers/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Verify password is not included
        for customer in data:
            assert 'password' not in customer
    
    def test_get_customer_by_id(self, client, test_customer):
        """Test getting specific customer by ID."""
        response = client.get(f'/customers/{test_customer.customer_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == test_customer.email
        assert 'password' not in data
    
    def test_get_nonexistent_customer(self, client):
        """Test getting customer that doesn't exist."""
        response = client.get('/customers/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['message'] == 'Customer not found'


class TestTokenUtilityFunctions:
    """Test token encoding and validation utilities."""
    
    def test_encode_token(self, app, test_customer):
        """Test token encoding creates valid token."""
        with app.app_context():
            token = encode_token(test_customer.customer_id)
            
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0
    
    def test_token_contains_customer_id(self, app, client, test_customer, auth_token):
        """Test that token correctly identifies customer."""
        # Use token to access profile
        response = client.get(
            '/customers/profile',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['customer_id'] == test_customer.customer_id


class TestTokenSecurity:
    """Test token security features."""
    
    def test_token_different_for_different_customers(self, app, client):
        """Test that different customers get different tokens."""
        # Register first customer
        client.post('/customers/register', json={
            'first_name': 'User',
            'last_name': 'One',
            'email': 'user1@example.com',
            'password': 'password123'
        })
        
        # Register second customer
        client.post('/customers/register', json={
            'first_name': 'User',
            'last_name': 'Two',
            'email': 'user2@example.com',
            'password': 'password123'
        })
        
        # Login both customers
        response1 = client.post('/customers/login', json={
            'email': 'user1@example.com',
            'password': 'password123'
        })
        token1 = response1.get_json()['auth_token']
        
        response2 = client.post('/customers/login', json={
            'email': 'user2@example.com',
            'password': 'password123'
        })
        token2 = response2.get_json()['auth_token']
        
        # Tokens should be different
        assert token1 != token2
    
    def test_cannot_access_other_customer_data(self, app, client, test_customer, auth_token):
        """Test that one customer cannot access another customer's tickets."""
        # Create second customer with vehicle and ticket
        from application.models import Customer, Vehicle, ServiceTicket
        from application.extensions import db
        
        customer2 = Customer(
            first_name='Other',
            last_name='Customer',
            email='other@example.com',
            password='password123'
        )
        db.session.add(customer2)
        db.session.commit()
        
        vehicle2 = Vehicle(
            customer_id=customer2.customer_id,
            vin='OTHER123VIN',
            make='Honda',
            model='Civic',
            year=2019
        )
        db.session.add(vehicle2)
        db.session.commit()
        
        ticket2 = ServiceTicket(
            vehicle_id=vehicle2.vehicle_id,
            customer_id=customer2.customer_id,
            status='OPEN',
            problem_description='Brake check'
        )
        db.session.add(ticket2)
        db.session.commit()
        
        # Use first customer's token to get tickets
        response = client.get(
            '/customers/my-tickets',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Should only see their own tickets (none in this case)
        assert data['customer_id'] == test_customer.customer_id
        # Should not see customer2's tickets
        ticket_ids = [t['ticket_id'] for t in data['tickets']]
        assert ticket2.ticket_id not in ticket_ids
