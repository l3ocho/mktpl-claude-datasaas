# Deploy Pipeline Integration

Add to your project's CLAUDE.md:

## Deployment Management (ops-deploy-pipeline)

This project uses the **ops-deploy-pipeline** plugin for Docker Compose deployment configuration, validation, and rollback planning.

### Available Commands

| Command | Description |
|---------|-------------|
| `/deploy setup` | Setup deployment configuration for this project |
| `/deploy generate` | Generate docker-compose.yml, Caddyfile, systemd units |
| `/deploy validate` | Validate configs for correctness and best practices |
| `/deploy env` | Manage .env.development / .env.production files |
| `/deploy check` | Pre-deployment health check (system resources, ports, Docker) |
| `/deploy rollback` | Generate rollback plan with volume backup steps |

### Usage Guidelines

- Run `/deploy setup` first to establish project deployment profile
- Use `/deploy generate` to create initial configs, then customize
- Always run `/deploy validate` before deploying to catch issues
- Use `/deploy check` on the target server before `docker compose up`
- Generate a `/deploy rollback` plan before any production deployment
- Never commit `.env.production` or `.env.staging` to version control
