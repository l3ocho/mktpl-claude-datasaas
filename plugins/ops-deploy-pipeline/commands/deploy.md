---
name: deploy
description: Deployment management — type /deploy <action> for commands
---

# /deploy

CI/CD deployment pipeline management for Docker Compose and self-hosted infrastructure.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/ops-deploy-pipeline:deploy-setup` | Interactive setup wizard for deployment configuration |
| `generate` | `/ops-deploy-pipeline:deploy-generate` | Generate docker-compose.yml, Caddyfile, and systemd units |
| `validate` | `/ops-deploy-pipeline:deploy-validate` | Validate deployment configs for correctness and best practices |
| `env` | `/ops-deploy-pipeline:deploy-env` | Manage environment-specific config files (.env.development, .env.production) |
| `check` | `/ops-deploy-pipeline:deploy-check` | Pre-deployment health check (disk, memory, ports, DNS, Docker) |
| `rollback` | `/ops-deploy-pipeline:deploy-rollback` | Generate rollback plan for a deployment |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/deploy generate`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/ops-deploy-pipeline:deploy-generate`)
