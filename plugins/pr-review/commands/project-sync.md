---
description: Sync project configuration with current git remote - use after changing repository location
---

# Project Sync (PR Review)

Updates project configuration when the git remote URL has changed.

**Use this when:**
- Repository was moved to a different organization
- Repository was renamed
- Git remote URL changed
- SessionStart hook detected a mismatch

---

## Step 1: Verify System Configuration

```bash
cat ~/.config/claude/gitea.env 2>/dev/null | grep -v "^#" | grep -v "PASTE_YOUR" | grep "GITEA_TOKEN=" && echo "SYSTEM_OK" || echo "SYSTEM_MISSING"
```

**If SYSTEM_MISSING:** Run `/initial-setup` first.

---

## Step 2: Read Current .env

```bash
cat .env 2>/dev/null
```

Extract `GITEA_ORG` and `GITEA_REPO` values.

**If missing:** Redirect to `/project-init`.

---

## Step 3: Detect Git Remote

```bash
git remote get-url origin 2>/dev/null
```

Extract organization and repository from URL.

---

## Step 4: Compare Values

| Scenario | Action |
|----------|--------|
| **Match** | "Configuration in sync" - exit |
| **Mismatch** | Show diff, proceed to validation |

---

## Step 5: Validate via Gitea API

```bash
source ~/.config/claude/gitea.env
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITEA_TOKEN" "$GITEA_URL/api/v1/repos/<NEW_ORG>/<NEW_REPO>"
```

| Code | Action |
|------|--------|
| **200** | Verified - proceed to update |
| **404** | Not found - ask to confirm |
| **401/403** | Permission issue - warn |

---

## Step 6: Confirm and Update

Use AskUserQuestion to confirm, then update .env:

```bash
sed -i 's/^GITEA_ORG=.*/GITEA_ORG=<NEW_ORG>/' .env
sed -i 's/^GITEA_REPO=.*/GITEA_REPO=<NEW_REPO>/' .env
```

---

## Step 7: Confirm Success

```
╔══════════════════════════════════════════════════════════════╗
║              CONFIGURATION UPDATED                           ║
╠══════════════════════════════════════════════════════════════╣
║ Organization:  <NEW_ORG>                                     ║
║ Repository:    <NEW_REPO>                                    ║
╚══════════════════════════════════════════════════════════════╝
```
