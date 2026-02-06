# Design: ops-deploy-pipeline

**Domain:** `ops`
**Target Version:** v9.7.0

## Purpose

CI/CD deployment pipeline management for Docker Compose and systemd-based services. Generates deployment configurations, validates pipeline definitions, and manages environment-specific settings. Tailored for self-hosted infrastructure (not cloud-native).

## Target Users

- Self-hosted service operators (Raspberry Pi, VPS, bare-metal)
- Teams deploying via Docker Compose
- Projects needing environment-specific configuration management

## Commands

| Command | Description |
|---------|-------------|
| `/deploy setup` | Setup wizard — detect deployment method, configure targets |
| `/deploy generate` | Generate docker-compose.yml, Caddyfile entries, systemd units |
| `/deploy validate` | Validate deployment configs (ports, volumes, networks, env vars) |
| `/deploy env` | Manage environment-specific config files (.env.production, etc.) |
| `/deploy check` | Pre-deployment health check (disk, memory, port conflicts) |
| `/deploy rollback` | Generate rollback plan for a deployment |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `deploy-planner` | sonnet | default | Configuration generation, rollback planning |
| `deploy-validator` | haiku | plan | Read-only validation of configs and pre-flight checks |

## Skills

| Skill | Purpose |
|-------|---------|
| `compose-patterns` | Docker Compose best practices, multi-service patterns |
| `caddy-conventions` | Caddyfile reverse proxy patterns, subdomain routing |
| `env-management` | Environment variable management across environments |
| `health-checks` | Pre-deployment system health validation |
| `rollback-patterns` | Deployment rollback strategies |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required initially.** Could add SSH-based remote execution MCP server in the future for remote deployment.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| cmdb-assistant | Deployment targets pulled from NetBox device inventory |
| ops-release-manager | Release tags trigger deployment preparation |
| projman | Issue labels: `Component/Infra`, `Tech/Docker`, `Tech/Caddy` |
| code-sentinel | Security scan of deployment configs (exposed ports, secrets in env) |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~700 |
| Dispatch file (`deploy.md`) | ~200 |
| 6 commands (avg) | ~3,600 |
| 2 agents | ~1,200 |
| 6 skills | ~2,500 |
| **Total** | **~8,200** |

## Open Questions

- Should this support Kubernetes/Helm for users who need it?
- SSH-based remote execution via MCP server for actual deployments?
