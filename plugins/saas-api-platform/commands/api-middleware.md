---
name: api middleware
description: Add and configure API middleware
agent: api-architect
---

# /api middleware - Middleware Manager

## Skills to Load

- skills/middleware-catalog.md
- skills/framework-detection.md
- skills/visual-header.md

## Visual Output

Display header: `API-PLATFORM - Middleware`

## Usage

```
/api middleware <action> [<type>] [--options]
```

**Actions:**
- `add <type>` - Add middleware to the application
- `list` - List currently configured middleware
- `remove <type>` - Remove middleware configuration

**Middleware Types:**
- `auth` - Authentication (JWT, OAuth2, API key)
- `cors` - Cross-Origin Resource Sharing
- `rate-limit` - Rate limiting per client/IP
- `logging` - Request/response logging
- `error-handler` - Global error handling and formatting
- `validation` - Request body/query validation

## Process

### 1. Detect Framework

Read `.api-platform.json` to determine target framework. Middleware implementation differs significantly between FastAPI and Express.

### 2. Add Middleware (`add` action)

**Auth Middleware:**
- Ask user for auth type: JWT Bearer, OAuth2, API key header
- Generate middleware file with token validation logic
- Add dependency/middleware registration to app
- Create auth utility functions (decode token, verify permissions)
- Generate `.env.example` entries for secrets (JWT_SECRET, etc.)

**CORS Middleware:**
- Ask for allowed origins (default: `["*"]` for development)
- Configure allowed methods, headers, credentials
- Set max_age for preflight caching
- FastAPI: `CORSMiddleware` configuration
- Express: `cors` package configuration

**Rate Limiting:**
- Ask for rate limit strategy: fixed window, sliding window, token bucket
- Configure limits per endpoint or global (requests/minute)
- Set burst allowance
- Configure response headers (X-RateLimit-Limit, X-RateLimit-Remaining)
- FastAPI: `slowapi` or custom middleware
- Express: `express-rate-limit` package

**Logging:**
- Configure log format (JSON structured, Apache combined, custom)
- Set log levels per environment (debug for dev, info for prod)
- Include request ID generation and propagation
- Configure sensitive field masking (Authorization header, passwords)
- FastAPI: custom middleware with `structlog` or `logging`
- Express: `morgan` or `pino-http`

**Error Handler:**
- Global exception/error handler with consistent response format
- Map framework exceptions to HTTP status codes
- Include request ID in error responses
- Mask internal details in production mode
- Log full stack traces server-side

**Validation:**
- Request body validation using framework-native tools
- Query parameter validation and type coercion
- Custom validation error response format

### 3. List Middleware (`list` action)

Scan app configuration and display active middleware in execution order.

### 4. Remove Middleware (`remove` action)

Remove middleware registration and associated files. Warn about dependencies.

## Output Format

```
+----------------------------------------------------------------------+
|  API-PLATFORM - Middleware                                            |
+----------------------------------------------------------------------+

Action: add
Type: rate-limit
Framework: FastAPI

Files Created/Modified:
  [+] app/middleware/rate_limit.py    (rate limiter implementation)
  [~] app/main.py                    (middleware registered)
  [~] .env.example                   (RATE_LIMIT_PER_MINUTE added)

Configuration:
  Strategy:     Sliding window
  Global Limit: 60 requests/minute
  Burst:        10 additional
  Headers:      X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

Dependencies Added:
  slowapi>=0.1.9

Next Steps:
  - pip install slowapi
  - Configure RATE_LIMIT_PER_MINUTE in .env
  - Override per-endpoint limits in route decorators if needed
```

## Important Notes

- Middleware order matters; auth should run before rate-limiting
- CORS must be configured before route handlers
- Error handler should be the outermost middleware
- Rate limiting should use persistent store (Redis) in production
