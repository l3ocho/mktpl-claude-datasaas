---
name: deploy rollback
description: Generate a rollback plan to revert a deployment to the previous state
---

# /deploy rollback

Generate a rollback plan for reverting a deployment.

## Skills to Load

- `skills/visual-header.md`
- `skills/rollback-patterns.md`
- `skills/compose-patterns.md`

## Agent

Delegate to `agents/deploy-planner.md`.

## Usage

```
/deploy rollback [--service=<name>] [--dry-run] [--strategy=<recreate|blue-green>]
```

**Options:**
- `--service` - Target a specific service (default: entire stack)
- `--dry-run` - Show plan without executing
- `--strategy` - Rollback strategy: `recreate` (default) or `blue-green`

## Instructions

Execute `skills/visual-header.md` with context "Rollback Planning".

### Phase 1: Current State Capture

1. List running containers for the stack:
   ```bash
   docker compose ps
   ```
2. Record current image digests:
   ```bash
   docker compose images
   ```
3. Check for volume data that may need backup:
   ```bash
   docker volume ls --filter name=<stack>
   ```
4. Record current environment variables from `.env`
5. Save current `docker-compose.yml` hash for verification

### Phase 2: Previous State Detection

Attempt to identify the previous deployment state:

1. Check git history for previous `docker-compose.yml`:
   ```bash
   git log --oneline -5 -- docker-compose.yml
   ```
2. Check Docker image history for previous tags
3. Look for backup files: `docker-compose.yml.bak`, `.env.bak`
4. If no previous state found, warn user and ask for target state

### Phase 3: Rollback Plan Generation

Apply patterns from `skills/rollback-patterns.md`:

#### Strategy: recreate (default)
1. Stop current containers: `docker compose down`
2. Restore previous docker-compose.yml from git
3. Restore previous .env file
4. Pull previous images if needed
5. Start containers: `docker compose up -d`
6. Verify health checks pass

#### Strategy: blue-green
1. Start previous version alongside current (different ports)
2. Verify previous version health
3. Switch reverse proxy to point to previous version
4. Stop current version
5. Rename previous version to use standard ports

### Phase 4: Data Considerations

1. Identify services with persistent volumes (databases, file storage)
2. Check if database migrations were run (irreversible changes)
3. Recommend volume backup before rollback:
   ```bash
   docker run --rm -v <volume>:/data -v $(pwd):/backup alpine tar czf /backup/<volume>.tar.gz /data
   ```
4. Flag if rollback may cause data loss

### Phase 5: Output

```
## Rollback Plan

### Target
- Service: myapp-stack
- Current: v2.1.0 (deployed 2h ago)
- Rollback to: v2.0.3

### Steps
1. Backup database volume (estimated: 2min)
   docker run --rm -v myapp_db:/data -v $(pwd):/backup alpine tar czf /backup/db-backup.tar.gz /data
2. Stop current stack
   docker compose down
3. Restore previous config
   git checkout HEAD~1 -- docker-compose.yml
4. Start previous version
   docker compose up -d
5. Verify health
   docker compose ps

### Warnings
- Database migration v45 was applied — may need manual revert
- Volume myapp_uploads has 230MB of new data since last deploy

### Estimated Downtime
- Strategy: recreate — ~30 seconds
- Strategy: blue-green — ~0 seconds (requires port availability)
```

## User Request

$ARGUMENTS
