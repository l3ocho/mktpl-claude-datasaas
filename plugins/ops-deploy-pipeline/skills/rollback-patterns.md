# Rollback Patterns Skill

Strategies for reverting deployments safely with minimal data loss and downtime.

## Strategy: Recreate (Default)

Simple stop-and-restart with previous configuration.

### Steps

1. **Backup current state**
   ```bash
   cp docker-compose.yml docker-compose.yml.bak
   cp .env .env.bak
   docker compose images > current-images.txt
   ```

2. **Backup volumes with data**
   ```bash
   docker run --rm -v <volume_name>:/data -v $(pwd)/backups:/backup \
     alpine tar czf /backup/<volume_name>-$(date +%Y%m%d%H%M).tar.gz /data
   ```

3. **Stop current deployment**
   ```bash
   docker compose down
   ```

4. **Restore previous config**
   ```bash
   git checkout <previous_commit> -- docker-compose.yml .env
   ```

5. **Start previous version**
   ```bash
   docker compose pull
   docker compose up -d
   ```

6. **Verify health**
   ```bash
   docker compose ps
   docker compose logs --tail=20
   ```

### Estimated Downtime

- Small stack (1-3 services): 10-30 seconds
- Medium stack (4-8 services): 30-60 seconds
- Large stack with DB: 1-3 minutes (depends on DB startup)

## Strategy: Blue-Green

Zero-downtime rollback by running both versions simultaneously.

### Prerequisites

- Available ports for the alternate deployment
- Reverse proxy that can switch upstream targets
- No port conflicts between blue and green instances

### Steps

1. **Start previous version on alternate ports**
   - Modify docker-compose to use different host ports
   - Start with `docker compose -p <stack>-green up -d`

2. **Verify previous version health**
   - Hit health endpoints on alternate ports
   - Confirm service functionality

3. **Switch reverse proxy**
   - Update Caddyfile to point to green deployment
   - Reload Caddy: `docker exec caddy caddy reload --config /etc/caddy/Caddyfile`

4. **Stop current (blue) version**
   ```bash
   docker compose -p <stack>-blue down
   ```

5. **Rename green to primary**
   - Restore original ports in docker-compose
   - Recreate with standard project name

### Estimated Downtime

- Near zero: Only the Caddy reload (sub-second)

## Database Rollback Considerations

### Safe (Reversible)

- Data inserts only (can delete new rows)
- No schema changes
- Configuration changes in env vars

### Dangerous (May Cause Data Loss)

- Schema migrations that drop columns
- Data transformations (one-way)
- Index changes on large tables

### Mitigation

1. Always backup database volume before rollback
2. Check for migration files between versions
3. If schema changed, may need to restore from backup rather than rollback
4. Document migration reversibility in deploy notes

## Volume Backup and Restore

### Backup

```bash
docker run --rm \
  -v <volume>:/data:ro \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/<volume>.tar.gz -C /data .
```

### Restore

```bash
docker run --rm \
  -v <volume>:/data \
  -v $(pwd)/backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/<volume>.tar.gz -C /data"
```

## Post-Rollback Verification

1. All containers running: `docker compose ps`
2. Health checks passing: `docker compose ps --format json | grep -c healthy`
3. Logs clean: `docker compose logs --tail=50 --no-color`
4. Application responding: `curl -s http://localhost:<port>/health`
5. Data integrity: Spot-check recent records in database
