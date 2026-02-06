---
name: deploy env
description: Manage environment-specific configuration files for deployments
---

# /deploy env

Create and manage environment-specific configuration files.

## Skills to Load

- `skills/visual-header.md`
- `skills/env-management.md`

## Agent

Delegate to `agents/deploy-planner.md`.

## Usage

```
/deploy env [--action=<create|diff|sync|list>] [--env=<development|staging|production>]
```

**Actions:**
- `create` - Create a new environment config from .env.example (default)
- `diff` - Show differences between environment configs
- `sync` - Sync missing keys from .env.example to all environments
- `list` - List all environment files and their variable counts

## Instructions

Execute `skills/visual-header.md` with context "Environment Management".

### Action: create

1. Check `.env.example` exists as the source template
2. If missing, scan `docker-compose.yml` for referenced `${VARIABLES}` and create `.env.example`
3. Ask user which environment to create (development, staging, production)
4. Copy `.env.example` to `.env.<environment>`
5. For production, flag variables that need real values (API keys, passwords)
6. For development, suggest sensible defaults (localhost URLs, debug=true)
7. Warn user to never commit `.env.production` to version control
8. Verify `.gitignore` includes `.env.production` and `.env.staging`

### Action: diff

1. Read all `.env.*` files in the project
2. Compare variable names across environments
3. Report:
   - Variables present in one environment but not others
   - Variables with identical values across environments (potential issue)
   - Variables in docker-compose but missing from all env files
4. Display as a comparison table

### Action: sync

1. Read `.env.example` as the canonical list of variables
2. For each `.env.<environment>` file:
   - Identify missing variables
   - Append missing variables with placeholder values
   - Report what was added
3. Do NOT modify existing values

### Action: list

1. List all `.env*` files in the project
2. For each file, show:
   - Variable count
   - Last modified date
   - Whether all docker-compose referenced variables are present

## Output Format

```
## Environment Files

| File | Variables | Coverage | Status |
|------|-----------|----------|--------|
| .env.example | 12 | 100% | Template |
| .env.development | 12 | 100% | OK |
| .env.production | 10 | 83% | Missing 2 vars |

### Missing in .env.production
- DATABASE_URL (referenced in docker-compose.yml:15)
- REDIS_PASSWORD (referenced in docker-compose.yml:28)
```

## User Request

$ARGUMENTS
