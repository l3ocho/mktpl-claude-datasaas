---
description: Sync project configuration with current git remote - use after changing repository location or organization
---

# Project Sync

Updates project configuration when the git remote URL has changed (repository moved, renamed, or organization changed).

**Use this when:**
- You moved the repository to a different organization
- You renamed the repository
- You changed the git remote URL
- The SessionStart hook detected a mismatch

---

## Step 1: Verify System Configuration

```bash
cat ~/.config/claude/gitea.env 2>/dev/null | grep -v "^#" | grep -v "PASTE_YOUR" | grep "GITEA_API_TOKEN=" && echo "SYSTEM_OK" || echo "SYSTEM_MISSING"
```

**If SYSTEM_MISSING:** Stop and instruct user to run `/initial-setup` first.

---

## Step 2: Read Current Configuration

Read the current .env values:

```bash
cat .env 2>/dev/null
```

Extract current values:
- `CURRENT_ORG` from `GITEA_ORG=...`
- `CURRENT_REPO` from `GITEA_REPO=...`

**If .env doesn't exist or has no GITEA values:** Redirect to `/project-init`.

---

## Step 3: Detect Git Remote Values

Get the current git remote:

```bash
git remote get-url origin 2>/dev/null
```

Extract organization:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\/[^/]*$/\1/'
```

Extract repository:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\.git$/\1/' | sed 's/.*\/\([^/]*\)$/\1/'
```

---

## Step 4: Compare Values

Compare current .env values with detected git remote values:

| Scenario | Action |
|----------|--------|
| **Both match** | Display "Configuration is in sync" and exit |
| **Organization changed** | Proceed to Step 5 |
| **Repository changed** | Proceed to Step 5 |
| **Both changed** | Proceed to Step 5 |

**If already in sync:**

```
╔══════════════════════════════════════════════════════════════╗
║                  CONFIGURATION IN SYNC                       ║
╠══════════════════════════════════════════════════════════════╣
║ Organization:  <ORG_NAME>                                    ║
║ Repository:    <REPO_NAME>                                   ║
║ Git Remote:    matches .env                                  ║
╚══════════════════════════════════════════════════════════════╝
```

Exit here if in sync.

---

## Step 5: Show Detected Changes

Display the detected changes to the user:

```
╔══════════════════════════════════════════════════════════════╗
║               REPOSITORY CHANGE DETECTED                     ║
╠══════════════════════════════════════════════════════════════╣
║                    Current .env    │    Git Remote           ║
║ Organization:      <OLD_ORG>       │    <NEW_ORG>            ║
║ Repository:        <OLD_REPO>      │    <NEW_REPO>           ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 6: Validate New Repository via Gitea API

Verify the new repository exists and is accessible:

```bash
source ~/.config/claude/gitea.env
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITEA_API_TOKEN" "$GITEA_API_URL/repos/<NEW_ORG>/<NEW_REPO>"
```

| HTTP Code | Action |
|-----------|--------|
| **200** | Repository verified - proceed to Step 7 |
| **404** | Repository not found - ask user to confirm (Step 6a) |
| **401/403** | Permission issue - warn and ask to confirm |

### Step 6a: Confirm if API Validation Failed

Use AskUserQuestion:
- Question: "The new repository '<NEW_ORG>/<NEW_REPO>' was not found via API. Update configuration anyway?"
- Header: "Not Found"
- Options:
  - "Yes, update anyway (I'll fix the remote later)"
  - "No, let me fix the git remote first"
  - "Let me specify different values"

**If "specify different values":** Ask for correct org and repo, then re-validate.

---

## Step 7: Confirm Update

Use AskUserQuestion:
- Question: "Update project configuration to match git remote?"
- Header: "Confirm"
- Options:
  - "Yes, update .env (Recommended)"
  - "No, keep current configuration"

**If "No":** Exit without changes.

---

## Step 8: Update Configuration

Update the .env file with new values:

```bash
# Update GITEA_ORG
sed -i 's/^GITEA_ORG=.*/GITEA_ORG=<NEW_ORG>/' .env

# Update GITEA_REPO
sed -i 's/^GITEA_REPO=.*/GITEA_REPO=<NEW_REPO>/' .env
```

Alternatively, if sed doesn't work well, read the file, replace values, and write back.

---

## Step 9: Verify Update

Read the updated .env and display confirmation:

```
╔══════════════════════════════════════════════════════════════╗
║              CONFIGURATION UPDATED                           ║
╠══════════════════════════════════════════════════════════════╣
║ Organization:  <NEW_ORG>                                     ║
║ Repository:    <NEW_REPO>                                    ║
║ Status:        In sync with git remote                       ║
╚══════════════════════════════════════════════════════════════╝

Your project configuration has been updated.
MCP tools will now use the new repository.
```

---

## Troubleshooting

**"Repository not found" but it exists:**
- Check your Gitea token has access to the new organization
- Verify the repository name matches exactly (case-sensitive)
- Ensure your token has `repo` permissions

**Git remote URL is wrong:**
- Fix it first: `git remote set-url origin <correct-url>`
- Then run `/project-sync` again

**Want to revert the change:**
- Edit `.env` manually: `nano .env`
- Or run `/project-sync` after fixing the git remote
