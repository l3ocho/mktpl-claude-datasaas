---
name: deploy check
description: Pre-deployment health check — verify system readiness before deploying
---

# /deploy check

Run pre-deployment health checks to verify the target system is ready.

## Skills to Load

- `skills/visual-header.md`
- `skills/health-checks.md`

## Agent

Delegate to `agents/deploy-validator.md`.

## Usage

```
/deploy check [--service=<name>] [--verbose]
```

**Options:**
- `--service` - Check readiness for a specific service only
- `--verbose` - Show detailed output for each check

## Instructions

Execute `skills/visual-header.md` with context "Pre-Deployment Check".

### Phase 1: System Resources

Run system checks using Bash tool:

| Check | Command | Pass Condition |
|-------|---------|----------------|
| Disk space | `df -h /` | >10% free |
| Memory | `free -m` | >256MB available |
| CPU load | `uptime` | Load average < CPU count |
| Temperature | `vcgencmd measure_temp` (RPi) or `/sys/class/thermal/` | <70C |

### Phase 2: Docker Environment

| Check | Command | Pass Condition |
|-------|---------|----------------|
| Docker daemon | `docker info` | Running |
| Docker Compose | `docker compose version` | Installed |
| Disk usage | `docker system df` | <80% usage |
| Network | `docker network ls` | Expected networks exist |

### Phase 3: Port Availability

1. Read `docker-compose.yml` for all host port mappings
2. Check each port with `ss -tlnp | grep :<port>`
3. If port is in use, identify the process occupying it
4. Flag conflicts as Critical

### Phase 4: DNS and Network

| Check | Command | Pass Condition |
|-------|---------|----------------|
| DNS resolution | `nslookup <subdomain>` | Resolves correctly |
| Reverse proxy | `curl -s -o /dev/null -w "%{http_code}" http://localhost:80` | Caddy responding |
| Tailscale | `tailscale status` | Connected (if applicable) |

### Phase 5: Image Availability

1. Parse `docker-compose.yml` for image references
2. Run `docker pull --dry-run <image>` or `docker manifest inspect <image>`
3. Verify images exist and support the target architecture (arm64 for RPi)
4. Report image sizes and estimated pull time

### Phase 6: Report

```
## Pre-Deployment Check Report

### System Resources
[OK]  Disk: 45% used (54GB free)
[OK]  Memory: 1.2GB available
[OK]  CPU: Load 0.8 (4 cores)
[OK]  Temperature: 52C

### Docker
[OK]  Docker daemon: Running (v24.0.7)
[OK]  Compose: v2.21.0
[WARN] Docker disk: 72% used — consider pruning

### Ports
[OK]  8080 — Available
[FAIL] 3000 — In use by grafana (PID 1234)

### Network
[OK]  DNS: myapp.hotport resolves
[OK]  Caddy: Responding on :80

### Images
[OK]  postgres:16-alpine — arm64 available (89MB)
[WARN] custom-app:latest — No arm64 manifest found

### Summary
- Passed: 10 | Warnings: 2 | Failed: 1
- Status: NOT READY — fix port conflict on 3000
```

## User Request

$ARGUMENTS
