# ops-deploy-pipeline

CI/CD deployment pipeline management for Docker Compose and self-hosted infrastructure.

## Overview

This plugin provides deployment configuration generation, validation, environment management, and rollback planning for services running on Docker Compose with Caddy reverse proxy. It is designed for self-hosted infrastructure, particularly Raspberry Pi and ARM64 targets.

## Commands

| Command | Description |
|---------|-------------|
| `/deploy setup` | Interactive setup wizard for deployment configuration |
| `/deploy generate` | Generate docker-compose.yml, Caddyfile, and systemd units |
| `/deploy validate` | Validate deployment configs for correctness and best practices |
| `/deploy env` | Manage environment-specific config files |
| `/deploy check` | Pre-deployment health check (disk, memory, ports, DNS, Docker) |
| `/deploy rollback` | Generate rollback plan for a deployment |

## Agents

| Agent | Model | Mode | Purpose |
|-------|-------|------|---------|
| deploy-planner | sonnet | default | Configuration generation and rollback planning |
| deploy-validator | haiku | plan | Read-only validation and health checks |

## Skills

| Skill | Description |
|-------|-------------|
| compose-patterns | Docker Compose best practices and multi-service patterns |
| caddy-conventions | Caddyfile reverse proxy and subdomain routing patterns |
| env-management | Environment variable management across deployment stages |
| health-checks | Pre-deployment system health verification |
| rollback-patterns | Deployment rollback strategies and data safety |
| visual-header | Standard command output header |

## Architecture

```
plugins/ops-deploy-pipeline/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy.md              # Dispatch file
│   ├── deploy-setup.md
│   ├── deploy-generate.md
│   ├── deploy-validate.md
│   ├── deploy-env.md
│   ├── deploy-check.md
│   └── deploy-rollback.md
├── agents/
│   ├── deploy-planner.md
│   └── deploy-validator.md
├── skills/
│   ├── compose-patterns.md
│   ├── caddy-conventions.md
│   ├── env-management.md
│   ├── health-checks.md
│   ├── rollback-patterns.md
│   └── visual-header.md
├── claude-md-integration.md
└── README.md
```

## License

MIT License - Part of the Leo Claude Marketplace.
