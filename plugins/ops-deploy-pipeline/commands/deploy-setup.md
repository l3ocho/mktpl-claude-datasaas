---
name: deploy setup
description: Interactive setup wizard for deployment pipeline configuration
---

# /deploy setup

Configure the ops-deploy-pipeline plugin for a project.

## Skills to Load

- `skills/visual-header.md`
- `skills/compose-patterns.md`

## Agent

Delegate to `agents/deploy-planner.md`.

## Usage

```
/deploy setup
```

## Instructions

Execute `skills/visual-header.md` with context "Setup Wizard".

### Phase 1: Project Detection

1. Read the current directory for existing configuration files:
   - `docker-compose.yml` or `docker-compose.yaml`
   - `Caddyfile` or `caddy/Caddyfile`
   - `.env`, `.env.example`, `.env.production`, `.env.development`
   - `systemd/*.service` files
2. Report what was found and what is missing

### Phase 2: Deployment Profile

Ask user to select deployment profile:

| Profile | Description |
|---------|-------------|
| **single-service** | One container, one reverse proxy entry |
| **multi-service** | Multiple containers with shared network |
| **full-stack** | Application + database + cache + reverse proxy |

### Phase 3: Infrastructure Target

Collect target information:
1. **Hostname** - Server hostname (e.g., `hotport`)
2. **Subdomain** - Service subdomain (e.g., `myapp.hotport`)
3. **Port** - Internal service port
4. **Network mode** - Tailscale, local, or both

### Phase 4: Generate Scaffold

Based on profile and target:
1. Create `deploy/` directory if it does not exist
2. Generate `.env.example` with documented variables
3. Create deployment checklist in `deploy/CHECKLIST.md`
4. Report next steps to user

### Completion Summary

```
DEPLOY-PIPELINE SETUP COMPLETE

Profile:       multi-service
Target:        myapp.hotport
Config Dir:    deploy/

Next steps:
- /deploy generate     Generate docker-compose.yml and Caddyfile
- /deploy env          Create environment-specific configs
- /deploy validate     Validate generated configs
```

## User Request

$ARGUMENTS
