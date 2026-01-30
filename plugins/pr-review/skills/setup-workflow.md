# Setup Workflow

## Configuration Hierarchy

| Level | Location | Contents |
|-------|----------|----------|
| System | `~/.config/claude/gitea.env` | API URL, token (shared across projects) |
| Project | `.env` in project root | Org, repo name (per project) |

## System Configuration

### Check Existing

```bash
cat ~/.config/claude/gitea.env 2>/dev/null | grep -v "^#" | grep "GITEA_API_TOKEN=" && echo "OK" || echo "MISSING"
```

### Create New

```bash
mkdir -p ~/.config/claude
cat > ~/.config/claude/gitea.env << 'EOF'
# Gitea API Configuration
GITEA_API_URL=https://your-gitea-server.com
GITEA_API_TOKEN=PASTE_YOUR_TOKEN_HERE
EOF
chmod 600 ~/.config/claude/gitea.env
```

### Token Generation

1. Gitea: Settings > Applications > Generate New Token
2. Required scopes: `repo`, `read:org`, `read:user`

## Project Configuration

### Auto-Detect from Git Remote

Extract organization:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\/[^/]*$/\1/'
```

Extract repository:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\.git$/\1/' | sed 's/.*\/\([^/]*\)$/\1/'
```

### Validate via API

```bash
source ~/.config/claude/gitea.env
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITEA_API_TOKEN" "$GITEA_API_URL/repos/<org>/<repo>"
```

| Code | Meaning |
|------|---------|
| 200 | Repository verified |
| 404 | Not found - check org/repo names |
| 401/403 | Auth issue - check token |

### Create/Update .env

```bash
# New file
cat > .env << EOF
GITEA_ORG=<org>
GITEA_REPO=<repo>
EOF

# Or append to existing
echo "GITEA_ORG=<org>" >> .env
echo "GITEA_REPO=<repo>" >> .env
```

## PR Review Settings (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `PR_REVIEW_CONFIDENCE_THRESHOLD` | `0.7` | Minimum confidence to report |
| `PR_REVIEW_AUTO_SUBMIT` | `false` | Auto-submit reviews to Gitea |

## Sync Workflow

When git remote changes:

1. Detect new org/repo from git remote
2. Compare with .env values
3. Validate new values via API
4. Update .env with sed:

```bash
sed -i 's/^GITEA_ORG=.*/GITEA_ORG=<new_org>/' .env
sed -i 's/^GITEA_REPO=.*/GITEA_REPO=<new_repo>/' .env
```

## Shared with projman

The Gitea MCP server is shared with the projman plugin. If projman is already configured, system-level setup can be skipped.

Check for projman:
```bash
find ~/.claude ~/.config/claude -name "projman" -type d 2>/dev/null | head -1
```
