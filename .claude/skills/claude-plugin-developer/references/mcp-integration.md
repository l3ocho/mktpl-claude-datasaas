# MCP Server Integration

Comprehensive guide for integrating Model Context Protocol (MCP) servers with Claude plugins.

## MCP Overview

MCP servers provide structured interfaces to external tools and services, enabling Claude to interact with databases, APIs, and other systems through a standardized protocol.

## Basic Configuration

### .mcp.json Structure
```json
{
  "name": "restaurant-data-server",
  "version": "1.0.0",
  "description": "MCP server for restaurant database access",
  "command": "python",
  "args": ["servers/restaurant_mcp.py"],
  "env": {
    "DATABASE_URL": "${RESTAURANT_DB_URL}",
    "API_KEY": "${RESTAURANT_API_KEY}"
  },
  "capabilities": {
    "resources": true,
    "tools": true,
    "subscriptions": true
  }
}
```

## Server Implementation

### Python MCP Server
```python
#!/usr/bin/env python3
# servers/restaurant_mcp.py

import asyncio
import json
from typing import Any, Dict, List
from mcp import MCPServer, Resource, Tool

class RestaurantMCPServer(MCPServer):
    def __init__(self):
        super().__init__("restaurant-data-server")
        self.setup_tools()
        self.setup_resources()
    
    def setup_tools(self):
        @self.tool("get_sales_data")
        async def get_sales_data(date: str, location: str = None) -> Dict:
            """Retrieve sales data for specified date and location"""
            # Implementation
            return {
                "date": date,
                "location": location,
                "total_sales": 15420.50,
                "transactions": 342
            }
        
        @self.tool("update_inventory")
        async def update_inventory(item_id: str, quantity: int) -> Dict:
            """Update inventory levels for an item"""
            # Implementation
            return {
                "item_id": item_id,
                "new_quantity": quantity,
                "status": "updated"
            }
    
    def setup_resources(self):
        @self.resource("menu_items")
        async def get_menu_items() -> List[Resource]:
            """List all menu items"""
            items = await fetch_menu_from_db()
            return [
                Resource(
                    id=f"menu_item_{item['id']}",
                    name=item['name'],
                    description=f"Menu item: {item['name']}",
                    metadata={"price": item['price'], "category": item['category']}
                )
                for item in items
            ]

if __name__ == "__main__":
    server = RestaurantMCPServer()
    asyncio.run(server.run())
```

### Node.js MCP Server
```javascript
#!/usr/bin/env node
// servers/restaurant_mcp.js

const { MCPServer, Tool, Resource } = require('@modelcontextprotocol/server');

class RestaurantMCPServer extends MCPServer {
  constructor() {
    super('restaurant-data-server');
    this.setupTools();
    this.setupResources();
  }
  
  setupTools() {
    this.registerTool(new Tool({
      name: 'get_sales_data',
      description: 'Retrieve sales data',
      parameters: {
        type: 'object',
        properties: {
          date: { type: 'string', format: 'date' },
          location: { type: 'string' }
        },
        required: ['date']
      },
      handler: async ({ date, location }) => {
        // Implementation
        return {
          date,
          location,
          total_sales: 15420.50,
          transactions: 342
        };
      }
    }));
  }
  
  setupResources() {
    this.registerResourceProvider({
      pattern: /^menu_items$/,
      handler: async () => {
        const items = await this.fetchMenuFromDB();
        return items.map(item => ({
          id: `menu_item_${item.id}`,
          name: item.name,
          content: JSON.stringify(item, null, 2),
          mimeType: 'application/json'
        }));
      }
    });
  }
}

const server = new RestaurantMCPServer();
server.start();
```

## Tool Definitions

### Tool Schema
```json
{
  "name": "analyze_customer_feedback",
  "description": "Analyze customer feedback sentiment",
  "parameters": {
    "type": "object",
    "properties": {
      "feedback_id": {
        "type": "string",
        "description": "Unique feedback identifier"
      },
      "include_suggestions": {
        "type": "boolean",
        "default": true,
        "description": "Include improvement suggestions"
      }
    },
    "required": ["feedback_id"]
  }
}
```

### Complex Tool Example
```python
@server.tool("generate_report")
async def generate_report(
    report_type: str,
    start_date: str,
    end_date: str,
    format: str = "pdf",
    filters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Generate comprehensive business report
    
    Args:
        report_type: Type of report (sales, inventory, customer)
        start_date: Report start date (YYYY-MM-DD)
        end_date: Report end date (YYYY-MM-DD)
        format: Output format (pdf, excel, json)
        filters: Additional filters to apply
    
    Returns:
        Report data and download URL
    """
    # Validate inputs
    if not validate_date_range(start_date, end_date):
        raise ValueError("Invalid date range")
    
    # Generate report
    report_data = await compile_report_data(
        report_type, start_date, end_date, filters
    )
    
    # Format output
    if format == "pdf":
        url = await generate_pdf_report(report_data)
    elif format == "excel":
        url = await generate_excel_report(report_data)
    else:
        url = await save_json_report(report_data)
    
    return {
        "report_type": report_type,
        "period": f"{start_date} to {end_date}",
        "download_url": url,
        "summary": report_data.get("summary", {})
    }
```

## Resource Management

### Static Resources
```python
@server.resource("config/database_schema")
async def get_database_schema() -> Resource:
    """Provide database schema documentation"""
    schema = load_schema_file()
    return Resource(
        id="database_schema",
        name="Restaurant Database Schema",
        content=schema,
        mimeType="text/markdown"
    )
```

### Dynamic Resources
```python
@server.resource_pattern(r"^orders/(\d{4}-\d{2}-\d{2})$")
async def get_daily_orders(date: str) -> List[Resource]:
    """Get orders for a specific date"""
    orders = await fetch_orders_by_date(date)
    return [
        Resource(
            id=f"order_{order['id']}",
            name=f"Order #{order['number']}",
            content=json.dumps(order, indent=2),
            mimeType="application/json",
            metadata={
                "customer": order['customer_name'],
                "total": order['total_amount'],
                "status": order['status']
            }
        )
        for order in orders
    ]
```

### Subscription Resources
```python
@server.subscription("live_orders")
async def subscribe_to_orders(callback):
    """Subscribe to live order updates"""
    async def order_handler(order):
        await callback(Resource(
            id=f"live_order_{order['id']}",
            name=f"New Order #{order['number']}",
            content=json.dumps(order),
            mimeType="application/json"
        ))
    
    # Register handler with order system
    order_system.on_new_order(order_handler)
    
    # Return unsubscribe function
    return lambda: order_system.off_new_order(order_handler)
```

## Security Implementation

### Authentication
```python
class SecureRestaurantServer(MCPServer):
    def __init__(self):
        super().__init__("secure-restaurant-server")
        self.auth_token = os.environ.get("MCP_AUTH_TOKEN")
    
    async def authenticate(self, request):
        """Validate authentication token"""
        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {self.auth_token}":
            raise AuthenticationError("Invalid token")
    
    async def handle_request(self, request):
        await self.authenticate(request)
        return await super().handle_request(request)
```

### Input Validation
```python
@server.tool("update_menu_item")
async def update_menu_item(item_id: str, updates: Dict) -> Dict:
    """Securely update menu item"""
    # Validate item_id format
    if not re.match(r"^[A-Z0-9]{8}$", item_id):
        raise ValueError("Invalid item ID format")
    
    # Validate allowed fields
    allowed_fields = {"name", "price", "description", "category"}
    invalid_fields = set(updates.keys()) - allowed_fields
    if invalid_fields:
        raise ValueError(f"Invalid fields: {invalid_fields}")
    
    # Validate data types
    if "price" in updates:
        if not isinstance(updates["price"], (int, float)):
            raise TypeError("Price must be numeric")
        if updates["price"] < 0:
            raise ValueError("Price cannot be negative")
    
    # Apply updates
    result = await db.update_menu_item(item_id, updates)
    return {"status": "success", "updated": result}
```

### Rate Limiting
```python
from functools import wraps
import time

def rate_limit(max_calls=10, time_window=60):
    calls = {}
    
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            client_id = kwargs.get('client_id', 'default')
            now = time.time()
            
            # Clean old calls
            calls[client_id] = [
                t for t in calls.get(client_id, [])
                if now - t < time_window
            ]
            
            # Check rate limit
            if len(calls[client_id]) >= max_calls:
                raise RateLimitError(f"Rate limit exceeded: {max_calls}/{time_window}s")
            
            # Record call
            calls[client_id].append(now)
            
            # Execute function
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator

# Usage
@server.tool("expensive_operation")
@rate_limit(max_calls=5, time_window=300)
async def expensive_operation(data: str) -> Dict:
    """Rate-limited expensive operation"""
    result = await perform_expensive_calculation(data)
    return {"result": result}
```

## Error Handling

### Graceful Errors
```python
@server.tool("process_order")
async def process_order(order_data: Dict) -> Dict:
    try:
        # Validate order
        validation_result = validate_order(order_data)
        if not validation_result.is_valid:
            return {
                "status": "error",
                "error_code": "INVALID_ORDER",
                "message": validation_result.message,
                "fields": validation_result.invalid_fields
            }
        
        # Process order
        result = await order_processor.process(order_data)
        return {
            "status": "success",
            "order_id": result.order_id,
            "estimated_time": result.estimated_time
        }
        
    except InventoryError as e:
        return {
            "status": "error",
            "error_code": "INSUFFICIENT_INVENTORY",
            "message": str(e),
            "available_items": e.available_items
        }
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {e}")
        return {
            "status": "error",
            "error_code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred"
        }
```

### Error Recovery
```python
class ResilientMCPServer(MCPServer):
    def __init__(self):
        super().__init__("resilient-server")
        self.db = None
        self.reconnect_attempts = 0
    
    async def ensure_connection(self):
        """Ensure database connection with retry logic"""
        if self.db and self.db.is_connected():
            return
        
        for attempt in range(3):
            try:
                self.db = await create_db_connection()
                self.reconnect_attempts = 0
                return
            except ConnectionError:
                await asyncio.sleep(2 ** attempt)
        
        raise ServiceUnavailableError("Cannot connect to database")
    
    async def handle_tool_call(self, tool_name, params):
        await self.ensure_connection()
        return await super().handle_tool_call(tool_name, params)
```

## Testing MCP Servers

### Unit Testing
```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_sales_data():
    server = RestaurantMCPServer()
    server.db = AsyncMock()
    server.db.query.return_value = [
        {"date": "2024-01-15", "total": 1000}
    ]
    
    result = await server.tools["get_sales_data"](
        date="2024-01-15",
        location="main"
    )
    
    assert result["total_sales"] == 1000
    server.db.query.assert_called_once()
```

### Integration Testing
```python
async def test_mcp_server_integration():
    # Start test server
    server = RestaurantMCPServer()
    test_port = 8765
    await server.start(port=test_port)
    
    # Create client
    client = MCPClient(f"http://localhost:{test_port}")
    
    # Test tool call
    result = await client.call_tool(
        "get_sales_data",
        {"date": "2024-01-15"}
    )
    
    assert result["status"] == "success"
    
    # Cleanup
    await server.stop()
```

### Mock Server for Development
```javascript
// servers/mock_restaurant_mcp.js
class MockRestaurantServer extends MCPServer {
  constructor() {
    super('mock-restaurant-server');
    this.setupMockTools();
  }
  
  setupMockTools() {
    this.registerTool({
      name: 'get_sales_data',
      handler: async ({ date }) => ({
        date,
        total_sales: Math.random() * 10000,
        transactions: Math.floor(Math.random() * 500)
      })
    });
  }
}
```

## Performance Optimization

### Caching
```python
from functools import lru_cache
from cachetools import TTLCache

class CachedMCPServer(MCPServer):
    def __init__(self):
        super().__init__("cached-server")
        self.cache = TTLCache(maxsize=100, ttl=300)
    
    @server.tool("get_analytics")
    async def get_analytics(self, date_range: str) -> Dict:
        # Check cache
        cache_key = f"analytics_{date_range}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Compute analytics
        result = await self.compute_analytics(date_range)
        
        # Store in cache
        self.cache[cache_key] = result
        return result
```

### Connection Pooling
```python
import asyncpg

class PooledMCPServer(MCPServer):
    def __init__(self):
        super().__init__("pooled-server")
        self.db_pool = None
    
    async def initialize(self):
        self.db_pool = await asyncpg.create_pool(
            database="restaurant_db",
            user="mcp_user",
            password=os.environ["DB_PASSWORD"],
            host="localhost",
            port=5432,
            min_size=5,
            max_size=20
        )
    
    async def query(self, sql, *args):
        async with self.db_pool.acquire() as conn:
            return await conn.fetch(sql, *args)
```

## Deployment

### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY servers/ ./servers/
COPY .mcp.json .

ENV PYTHONUNBUFFERED=1

CMD ["python", "servers/restaurant_mcp.py"]
```

### Systemd Service
```ini
# /etc/systemd/system/restaurant-mcp.service
[Unit]
Description=Restaurant MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/restaurant-mcp
Environment="DATABASE_URL=postgresql://localhost/restaurant"
ExecStart=/usr/bin/python3 /opt/restaurant-mcp/servers/restaurant_mcp.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Health Checks
```python
@server.tool("health_check")
async def health_check() -> Dict:
    """MCP server health check endpoint"""
    checks = {
        "server": "ok",
        "database": "unknown",
        "cache": "unknown"
    }
    
    # Check database
    try:
        await db.execute("SELECT 1")
        checks["database"] = "ok"
    except:
        checks["database"] = "error"
    
    # Check cache
    try:
        cache.get("test")
        checks["cache"] = "ok"
    except:
        checks["cache"] = "error"
    
    overall_status = "healthy" if all(
        v == "ok" for v in checks.values()
    ) else "unhealthy"
    
    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```