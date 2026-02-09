---
name: deploy
description: Deployment management — type /deploy <action> for commands
---

# /deploy

CI/CD deployment pipeline management for Docker Compose and self-hosted infrastructure.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/deploy setup` | Interactive setup wizard for deployment configuration |
| `/deploy generate` | Generate docker-compose.yml, Caddyfile, and systemd units |
| `/deploy validate` | Validate deployment configs for correctness and best practices |
| `/deploy env` | Manage environment-specific config files (.env.development, .env.production) |
| `/deploy check` | Pre-deployment health check (disk, memory, ports, DNS, Docker) |
| `/deploy rollback` | Generate rollback plan for a deployment |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
