# Environment Management Skill

Patterns for managing environment variables across deployment stages.

## File Naming Convention

| File | Purpose | Git Tracked |
|------|---------|-------------|
| `.env.example` | Template with placeholder values | Yes |
| `.env` | Local development defaults | No |
| `.env.development` | Development-specific overrides | No |
| `.env.staging` | Staging environment values | No |
| `.env.production` | Production secrets and config | No |

## .env.example Format

Document every variable with comments:

```bash
# Application Settings
APP_NAME=myapp
APP_PORT=8080
APP_DEBUG=false

# Database Configuration
# PostgreSQL connection string
DATABASE_URL=postgresql://user:password@db:5432/myapp
DATABASE_POOL_SIZE=5

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# External Services
# Generate at: https://example.com/api-keys
API_KEY=your-api-key-here
API_SECRET=your-secret-here
```

## Secret Handling Rules

1. **Never commit secrets** to version control
2. `.env.production` and `.env.staging` MUST be in `.gitignore`
3. Use placeholder values in `.env.example`: `your-api-key-here`, `changeme`, `<required>`
4. For shared team secrets, use a secrets manager or encrypted vault
5. Document where to obtain each secret in comments

## Docker Compose Integration

### Single env_file

```yaml
env_file:
  - .env
```

### Multi-environment

```yaml
env_file:
  - .env
  - .env.${DEPLOY_ENV:-development}
```

### Variable Interpolation

Docker Compose supports `${VAR:-default}` syntax:

```yaml
services:
  app:
    image: myapp:${APP_VERSION:-latest}
    ports:
      - "${APP_PORT:-8080}:8080"
```

## Environment Diff Checking

When comparing environments, check for:

1. **Missing variables** - Present in .env.example but absent in target
2. **Extra variables** - Present in target but not in .env.example (may be stale)
3. **Placeholder values** - Production still has `changeme` or `your-*-here`
4. **Identical secrets** - Same password used in dev and prod (security risk)

## Validation Checklist

- [ ] All docker-compose `${VAR}` references have corresponding entries
- [ ] No secrets in `.env.example`
- [ ] `.gitignore` excludes `.env.production` and `.env.staging`
- [ ] Production variables have real values (no placeholders)
- [ ] Database URLs point to correct hosts per environment
- [ ] Debug flags are `false` in production
