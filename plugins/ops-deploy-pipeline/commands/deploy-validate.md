---
name: deploy validate
description: Validate deployment configs for correctness, security, and best practices
---

# /deploy validate

Validate Docker Compose, Caddyfile, and systemd configurations.

## Skills to Load

- `skills/visual-header.md`
- `skills/compose-patterns.md`
- `skills/health-checks.md`

## Agent

Delegate to `agents/deploy-validator.md`.

## Usage

```
/deploy validate [--target=<compose|caddy|systemd|all>] [--strict]
```

**Options:**
- `--target` - Which config to validate (default: `all`)
- `--strict` - Treat warnings as errors

## Instructions

Execute `skills/visual-header.md` with context "Config Validation".

### Phase 1: File Discovery

Locate configuration files:
- `docker-compose.yml` / `docker-compose.yaml`
- `Caddyfile` or `caddy/Caddyfile`
- `systemd/*.service`
- `.env`, `.env.production`, `.env.development`

Report any expected files that are missing.

### Phase 2: Docker Compose Validation

Check against patterns from `skills/compose-patterns.md`:

| Check | Severity | Description |
|-------|----------|-------------|
| Valid YAML syntax | Critical | File must parse correctly |
| Image tags pinned | Warning | Avoid `latest` tag in production |
| Healthchecks defined | Warning | All services should have healthchecks |
| Restart policy set | Warning | Should be `unless-stopped` or `always` |
| Resource limits | Info | Memory/CPU limits recommended for constrained hosts |
| Network isolation | Warning | Services should use dedicated network, not `host` |
| Volume permissions | Warning | Bind mounts should have explicit read/write mode |
| No hardcoded secrets | Critical | Secrets must use env_file or Docker secrets |
| Port conflicts | Critical | No duplicate host port mappings |
| Dependency ordering | Info | Services with depends_on should use health conditions |

### Phase 3: Caddyfile Validation

| Check | Severity | Description |
|-------|----------|-------------|
| Valid syntax | Critical | Directives must be properly formatted |
| HTTPS configuration | Info | Automatic HTTPS or explicit cert paths |
| Reverse proxy targets | Warning | Target must match docker-compose service names |
| Security headers | Info | Recommend X-Frame-Options, CSP, HSTS |
| Duplicate routes | Critical | No conflicting route definitions |

### Phase 4: Environment File Validation

| Check | Severity | Description |
|-------|----------|-------------|
| .env.example exists | Warning | Template for required variables |
| No secrets in .env.example | Critical | Example file must use placeholders |
| All referenced vars defined | Critical | docker-compose env vars must have values |
| Consistent across environments | Info | Same keys in dev/staging/prod |

### Phase 5: Report

```
## Validation Report

### Critical (must fix)
- [file:line] Description of issue
  Fix: Recommended solution

### Warnings (should fix)
- [file:line] Description of issue
  Fix: Recommended solution

### Info (consider)
- [file:line] Description of improvement

### Summary
- Critical: X | Warnings: Y | Info: Z
- Status: PASS / FAIL
```

## User Request

$ARGUMENTS
