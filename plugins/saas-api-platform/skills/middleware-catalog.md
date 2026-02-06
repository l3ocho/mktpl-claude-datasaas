---
name: middleware-catalog
description: Common middleware patterns for auth, CORS, rate-limiting, logging, and error handling per framework
---

# Middleware Catalog

## Purpose

Reference catalog of middleware patterns for FastAPI and Express. This skill is loaded by the `api-architect` agent when adding or configuring middleware, ensuring correct implementation per framework.

---

## Middleware Execution Order

Middleware should be registered in this order (outermost to innermost):

1. **Error Handler** - Catches all unhandled exceptions
2. **CORS** - Must run before any route processing
3. **Request ID** - Generate unique ID for tracing
4. **Logging** - Log incoming request details
5. **Rate Limiting** - Reject excessive requests early
6. **Authentication** - Validate credentials
7. **Authorization** - Check permissions (often per-route)
8. **Validation** - Validate request body/params (often per-route)
9. **Route Handler** - Business logic

---

## Authentication Middleware

### JWT Bearer (FastAPI)
- Use `fastapi.security.HTTPBearer` dependency
- Decode token with `python-jose` or `PyJWT`
- Store decoded claims in request state
- Return 401 for missing/invalid/expired tokens
- Environment: `JWT_SECRET`, `JWT_ALGORITHM` (default HS256)

### JWT Bearer (Express)
- Use `express-jwt` or custom middleware
- Decode token from `Authorization: Bearer <token>` header
- Attach decoded user to `req.user`
- Return 401 for missing/invalid/expired tokens
- Environment: `JWT_SECRET`, `JWT_ALGORITHM`

### API Key
- Read from `X-API-Key` header
- Compare against stored keys (database or environment)
- Return 401 for missing key, 403 for invalid key

---

## CORS Middleware

### FastAPI
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)
```

### Express
```javascript
const cors = require('cors');
app.use(cors({
    origin: '*',                 // Restrict in production
    credentials: true,
    methods: ['GET','POST','PUT','PATCH','DELETE'],
    maxAge: 600,
}));
```

---

## Rate Limiting

### Strategies
- **Fixed window**: N requests per time window (simple, bursty at boundaries)
- **Sliding window**: Smooth rate enforcement (recommended)
- **Token bucket**: Allows controlled bursts

### Response Headers
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining in window
- `X-RateLimit-Reset`: Timestamp when limit resets

### Production Notes
- Use Redis as backend store for distributed rate limiting
- In-memory stores do not work with multiple server instances
- Consider different limits for authenticated vs anonymous users

---

## Logging Middleware

### Structured Logging Fields
Every request log entry should include:
- `request_id`: Unique identifier for tracing
- `method`: HTTP method
- `path`: Request path
- `status_code`: Response status
- `duration_ms`: Processing time
- `client_ip`: Client IP address
- `user_id`: Authenticated user ID (if available)

### Sensitive Field Masking
Never log: `Authorization` header values, request bodies containing `password`, `token`, `secret`, `credit_card` fields.

---

## Error Handler

### Standard Error Response
All errors must produce consistent JSON:
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable message",
        "request_id": "abc-123"
    }
}
```

### Exception Mapping
- Validation errors: 422 with field-level details
- Not found: 404 with resource type and ID
- Authentication: 401 with generic message (no details)
- Authorization: 403 with required permission
- Conflict: 409 with conflicting field
- Internal: 500 with request_id only (no stack traces in production)
