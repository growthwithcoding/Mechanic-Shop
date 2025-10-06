# Assignment 10 Testing Commands for PowerShell

## PowerShell Testing Commands

Since you're using PowerShell, use these commands instead of curl:

### 1. Create Inventory Parts

```powershell
# Create Oil Filter
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Oil Filter", "price": 15.99}' -ContentType "application/json"

# Create Brake Pads
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Brake Pads", "price": 45.50}' -ContentType "application/json"

# Create Air Filter
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Air Filter", "price": 22.00}' -ContentType "application/json"

# Create Spark Plugs
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Spark Plugs", "price": 32.99}' -ContentType "application/json"
```

### 2. List All Inventory

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method GET
```

### 3. Get Single Part

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/1" -Method GET
```

### 4. Update Part Price

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/1" -Method PUT -Body '{"price": 17.99}' -ContentType "application/json"
```

### 5. Create a Service Ticket (if you don't have one)

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/service-tickets/" -Method POST -Body '{"customer_email": "john.doe@example.com", "customer_name": "John Doe", "vehicle_make": "Toyota", "vehicle_model": "Camry", "vehicle_year": 2020, "problem_description": "Oil change needed", "priority": 3}' -ContentType "application/json"
```

### 6. Add Part to Service Ticket

```powershell
# Add Oil Filter (id=1) to Ticket (id=1)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/service-tickets/1/add-part/1" -Method POST
```

### 7. Delete a Part

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/4" -Method DELETE
```

## Quick Test Sequence

Run these commands in order to test everything:

```powershell
# 1. Create some inventory parts
Write-Host "Creating Oil Filter..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Oil Filter", "price": 15.99}' -ContentType "application/json"

Write-Host "`nCreating Brake Pads..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Brake Pads", "price": 45.50}' -ContentType "application/json"

Write-Host "`nCreating Air Filter..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method POST -Body '{"name": "Air Filter", "price": 22.00}' -ContentType "application/json"

# 2. List all parts
Write-Host "`n=== All Inventory Parts ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/" -Method GET

# 3. Get single part
Write-Host "`n=== Single Part (ID=1) ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/1" -Method GET

# 4. Update part price
Write-Host "`nUpdating Oil Filter price..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/inventory/1" -Method PUT -Body '{"price": 17.99}' -ContentType "application/json"

# 5. Create a service ticket
Write-Host "`nCreating Service Ticket..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/service-tickets/" -Method POST -Body '{"customer_email": "test@example.com", "customer_name": "Test User", "vehicle_make": "Honda", "vehicle_model": "Civic", "vehicle_year": 2021, "problem_description": "Regular maintenance", "priority": 2}' -ContentType "application/json"

# 6. Add part to ticket
Write-Host "`nAdding Oil Filter to Ticket..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/service-tickets/1/add-part/1" -Method POST

Write-Host "`nAdding Brake Pads to Ticket..." -ForegroundColor Green
Invoke-RestMethod -Uri "http://127.0.0.1:5000/service-tickets/1/add-part/2" -Method POST

Write-Host "`n=== Testing Complete! ===" -ForegroundColor Yellow
```

## Alternative: Use Postman (Recommended)

The easiest way to test is to use Postman:

1. Open Postman
2. Click "Import"
3. Select the file: `postman_exports/Mechanic_Shop_Assignment10_Collection.json`
4. All 25+ requests will be imported and organized
5. Run requests in the "Inventory" folder

## Using Windows curl.exe directly

If you have curl.exe installed (not the PowerShell alias), you can use it directly:

```powershell
curl.exe -X POST http://127.0.0.1:5000/inventory/ -H "Content-Type: application/json" -d "{\"name\": \"Oil Filter\", \"price\": 15.99}"
```

Note: You need to escape the quotes with backslashes when using curl.exe in PowerShell.
