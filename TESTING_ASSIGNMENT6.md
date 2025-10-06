# Assignment 6 Testing Guide - Rate Limiting and Caching

## Application Status
✅ Flask application running on: **http://127.0.0.1:5000**
✅ Flask-Limiter initialized (in-memory storage)
✅ Flask-Caching initialized (SimpleCache)

---

## Test Scenarios for Postman

### Test 1: Rate Limiting on POST /mechanics/

**Objective:** Verify that mechanic creation is limited to 5 requests per hour

**Steps:**
1. Open Postman
2. Create a new POST request to: `http://127.0.0.1:5000/mechanics/`
3. Set Headers:
   - `Content-Type: application/json`
4. Set Body (raw JSON):
   ```json
   {
     "name": "Test Mechanic 1",
     "email": "test1@example.com",
     "phone": "555-0001",
     "salary": 50000
   }
   ```
5. **Send the request 6 times in succession** (change the email/name each time to avoid duplicates)

**Expected Results:**
- **First 5 requests:** Should return `201 Created` with mechanic data
- **6th request:** Should return `429 Too Many Requests` with error message about rate limit exceeded

**Rate Limit:** 5 per hour per IP address

---

### Test 2: Rate Limiting on POST /service-tickets/

**Objective:** Verify that service ticket creation is limited to 10 requests per hour

**Steps:**
1. Create a new POST request to: `http://127.0.0.1:5000/service-tickets/`
2. Set Headers:
   - `Content-Type: application/json`
3. Set Body (raw JSON):
   ```json
   {
     "customer_name": "John Doe",
     "customer_email": "john@example.com",
     "customer_phone": "555-1234",
     "vehicle_make": "Toyota",
     "vehicle_model": "Camry",
     "vehicle_year": 2020,
     "description": "Oil change needed"
   }
   ```
4. **Send the request 11 times in succession** (change customer_email each time)

**Expected Results:**
- **First 10 requests:** Should return `201 Created` with ticket data
- **11th request:** Should return `429 Too Many Requests`

**Rate Limit:** 10 per hour per IP address

---

### Test 3: Caching on GET /mechanics/

**Objective:** Verify that mechanic list is cached for 60 seconds

**Steps:**
1. Create a new GET request to: `http://127.0.0.1:5000/mechanics/`
2. **First Request:**
   - Send the request
   - Note the response time (should query database)
   - Note the list of mechanics returned
3. **Immediately send 2-3 more requests within 60 seconds:**
   - These should be served from cache (faster response)
   - Should return the same data
4. **Create a new mechanic** using POST /mechanics/ (from Test 1)
5. **Send GET /mechanics/ again immediately:**
   - The new mechanic will NOT appear yet (cache is active)
6. **Wait 60+ seconds** and send GET /mechanics/ again:
   - Cache expired, database is queried again
   - New mechanic should now appear

**Expected Behavior:**
- Cache duration: **60 seconds**
- First request after cache expiry will hit database
- Subsequent requests within 60s serve from cache
- Cache doesn't invalidate on data changes (by design for this assignment)

---

### Test 4: Caching on GET /service-tickets/

**Objective:** Verify that service ticket list is cached for 30 seconds

**Steps:**
1. Create a new GET request to: `http://127.0.0.1:5000/service-tickets/`
2. **First Request:**
   - Send the request
   - Note the response time and ticket count
3. **Immediately send 2-3 more requests within 30 seconds:**
   - Should be faster (served from cache)
4. **Create a new ticket** using POST /service-tickets/
5. **Send GET /service-tickets/ immediately:**
   - New ticket won't appear yet (cache active)
6. **Wait 30+ seconds** and send GET /service-tickets/ again:
   - Cache expired, new ticket should appear

**Expected Behavior:**
- Cache duration: **30 seconds** (shorter than mechanics due to more frequent updates)
- Behavior similar to Test 3 but with shorter cache window

---

## Additional Tests

### Test 5: Rate Limit Headers (Optional)
Check the response headers from rate-limited endpoints:
- Look for headers like `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- These help clients know their rate limit status

### Test 6: Different Routes (No Limits)
Verify that other routes (GET requests, PUT, DELETE) work normally without rate limits:
- `GET /mechanics/<id>` - Should work without rate limits
- `PUT /mechanics/<id>` - No rate limit applied
- `DELETE /mechanics/<id>` - No rate limit applied

---

## Quick Reference

| Endpoint | Method | Rate Limit | Cache Duration | Purpose |
|----------|--------|------------|----------------|---------|
| `/mechanics/` | POST | 5/hour | N/A | Create mechanic |
| `/mechanics/` | GET | None | 60 seconds | List mechanics |
| `/service-tickets/` | POST | 10/hour | N/A | Create ticket |
| `/service-tickets/` | GET | None | 30 seconds | List tickets |

---

## Tips for Testing

1. **Rate Limiting:**
   - Use Postman's Collection Runner to send multiple requests quickly
   - Or manually click "Send" multiple times rapidly
   - To reset rate limits: Restart the Flask application

2. **Caching:**
   - Use a timer or watch to track 30/60 second intervals
   - Compare response times (cached responses are faster)
   - Create data between requests to see cache behavior

3. **Observing in Terminal:**
   - Watch the Flask terminal for database queries
   - Cached requests won't show database activity
   - Rate-limited requests will show in logs

---

## Success Criteria

✅ **Rate Limiting Works If:**
- 6th POST to /mechanics/ returns 429
- 11th POST to /service-tickets/ returns 429
- Error message mentions rate limit exceeded

✅ **Caching Works If:**
- Subsequent GET requests within cache time are faster
- Data changes don't appear until cache expires
- After cache expiry, new data appears

---

## Troubleshooting

**Issue:** All requests return 429 immediately
- **Solution:** Restart Flask app to reset in-memory rate limits

**Issue:** Cache seems to last longer than specified
- **Solution:** This is normal with SimpleCache, minor variations can occur

**Issue:** Can't see rate limit effects
- **Solution:** Make sure you're hitting the correct endpoints (POST, not GET)

---

## Notes

- Flask-Limiter warning about in-memory storage is expected for development
- In production, you'd use Redis or Memcached for distributed rate limiting
- SimpleCache is perfect for development but not recommended for production
- Rate limits are per IP address (127.0.0.1 in local testing)
