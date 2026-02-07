# Docker Compose Patterns Skill

Best practices and patterns for Docker Compose service definitions targeting self-hosted infrastructure.

## Service Naming

- Use lowercase with hyphens: `my-service`
- Prefix with stack name for multi-project hosts: `myapp-db`, `myapp-redis`
- Container name should match service name: `container_name: myapp-db`

## Network Isolation

Every stack should define its own bridge network:

```yaml
networks:
  app-network:
    driver: bridge
```

Services join the stack network. Only the reverse proxy entry point should be exposed to the host.

## Volume Management

- Use **named volumes** for data persistence (databases, uploads)
- Use **bind mounts** for configuration files only
- Set explicit permissions with `:ro` for read-only mounts
- Label volumes with `labels` for identification

```yaml
volumes:
  db-data:
    labels:
      com.project: myapp
      com.service: database
```

## Healthchecks

Every service MUST have a healthcheck:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Common healthcheck patterns:
- HTTP: `curl -f http://localhost:<port>/health`
- PostgreSQL: `pg_isready -U <user>`
- Redis: `redis-cli ping`
- MySQL: `mysqladmin ping -h localhost`

## Restart Policies

| Environment | Policy |
|-------------|--------|
| Development | `restart: "no"` |
| Production | `restart: unless-stopped` |
| Critical services | `restart: always` |

## Resource Limits

For Raspberry Pi (8GB RAM):

```yaml
deploy:
  resources:
    limits:
      memory: 256M
      cpus: '1.0'
    reservations:
      memory: 128M
```

## Dependency Ordering

Use healthcheck-aware dependencies:

```yaml
depends_on:
  db:
    condition: service_healthy
  redis:
    condition: service_started
```

## Environment Variables

Never inline secrets. Use `env_file`:

```yaml
env_file:
  - .env
  - .env.${DEPLOY_ENV:-development}
```

## Multi-Service Patterns

### Web App + Database + Cache

```yaml
services:
  app:
    image: myapp:1.0.0
    env_file: [.env]
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }
    networks: [app-network]

  db:
    image: postgres:16-alpine
    volumes: [db-data:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
    networks: [app-network]

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
    networks: [app-network]
```
