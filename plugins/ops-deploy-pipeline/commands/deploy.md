---
description: Deployment management — generate configs, validate pipelines, manage environments
---

# /deploy

CI/CD deployment pipeline management for Docker Compose and self-hosted infrastructure.

## Sub-commands

| Sub-command | Description |
|-------------|-------------|
| `/deploy setup` | Interactive setup wizard for deployment configuration |
| `/deploy generate` | Generate docker-compose.yml, Caddyfile, and systemd units |
| `/deploy validate` | Validate deployment configs for correctness and best practices |
| `/deploy env` | Manage environment-specific config files (.env.development, .env.production) |
| `/deploy check` | Pre-deployment health check (disk, memory, ports, DNS, Docker) |
| `/deploy rollback` | Generate rollback plan for a deployment |
