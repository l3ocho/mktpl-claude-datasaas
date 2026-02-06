---
name: deploy generate
description: Generate docker-compose.yml, Caddyfile, and systemd units for a service
---

# /deploy generate

Generate deployment configuration files from templates and project context.

## Skills to Load

- `skills/visual-header.md`
- `skills/compose-patterns.md`
- `skills/caddy-conventions.md`
- `skills/env-management.md`

## Agent

Delegate to `agents/deploy-planner.md`.

## Usage

```
/deploy generate [--target=<compose|caddy|systemd|all>] [--service=<name>]
```

**Targets:**
- `compose` - Generate docker-compose.yml only
- `caddy` - Generate Caddyfile snippet only
- `systemd` - Generate systemd service unit only
- `all` - Generate all configuration files (default)

## Instructions

Execute `skills/visual-header.md` with context "Config Generation".

### Phase 1: Context Analysis

1. Read existing project files to determine:
   - Application language/framework (Dockerfile, package.json, requirements.txt, go.mod)
   - Required services (database, cache, message queue)
   - Exposed ports
   - Volume requirements (data persistence, config files)
2. Check if `deploy/` directory exists from previous `/deploy setup`
3. Read `.env.example` if present for variable names

### Phase 2: Docker Compose Generation

Apply patterns from `skills/compose-patterns.md`:

1. **Service definition** - Image or build context, restart policy, healthcheck
2. **Network isolation** - Create dedicated network for the stack
3. **Volume management** - Named volumes for persistence, bind mounts for config
4. **Resource limits** - Memory and CPU limits appropriate for target platform
5. **Dependency ordering** - `depends_on` with `condition: service_healthy`
6. **Environment variables** - Reference `env_file` rather than inline secrets

### Phase 3: Caddyfile Generation

Apply patterns from `skills/caddy-conventions.md`:

1. **Subdomain routing** - `subdomain.hostname` block
2. **Reverse proxy** - Point to container:port with Docker network DNS
3. **Headers** - Security headers, CORS if needed
4. **Rate limiting** - Default rate limit for API endpoints

### Phase 4: Systemd Unit Generation (optional)

Generate `systemd/<service>.service` for non-Docker services:
1. Unit description and dependencies
2. ExecStart/ExecStop commands
3. Restart policy and watchdog
4. User/Group restrictions

### Phase 5: Output

1. Show generated files with syntax highlighting
2. Ask user to confirm before writing
3. Write files to appropriate locations
4. Display validation summary

## Output Format

```
## Generated Files

### docker-compose.yml
[content with annotations]

### Caddyfile snippet
[content with annotations]

### Summary
- Services: 3 (app, db, redis)
- Networks: 1 (app-network)
- Volumes: 2 (db-data, redis-data)
- Next: /deploy validate
```

## User Request

$ARGUMENTS
