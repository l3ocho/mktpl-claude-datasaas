---
description: Quick project setup - configures only project-level settings for PR review
---

# Project Initialization (PR Review)

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 PR-REVIEW · Project Setup                                     │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the setup.

Fast setup for a new project when system-level configuration is already complete.

**Use this when:**
- You've already run `/initial-setup` on this machine
- You're starting work on a new project/repository
- You just need to configure this project for PR reviews

---

## Pre-Flight Check

### Step 1: Verify System Configuration

```bash
cat ~/.config/claude/gitea.env 2>/dev/null | grep -v "^#" | grep -v "PASTE_YOUR" | grep "GITEA_API_TOKEN=" && echo "SYSTEM_OK" || echo "SYSTEM_MISSING"
```

**If SYSTEM_MISSING:**

---

**System configuration not found.**

Please run `/initial-setup` first to configure Gitea credentials.

---

**If SYSTEM_OK:** Continue.

---

## Project Setup

### Step 2: Verify Current Directory

```bash
pwd && git rev-parse --show-toplevel 2>/dev/null || echo "NOT_A_GIT_REPO"
```

### Step 3: Check Existing Configuration

```bash
cat .env 2>/dev/null | grep "GITEA_REPO=" || echo "NOT_CONFIGURED"
```

If already configured, ask if user wants to keep or reconfigure.

### Step 4: Detect Organization and Repository

Extract organization:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\/[^/]*$/\1/'
```

Extract repository:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\.git$/\1/' | sed 's/.*\/\([^/]*\)$/\1/'
```

### Step 5: Validate Repository via Gitea API

```bash
source ~/.config/claude/gitea.env
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITEA_API_TOKEN" "$GITEA_API_URL/repos/<detected-org>/<detected-repo>"
```

| HTTP Code | Action |
|-----------|--------|
| **200** | Auto-fill - "Verified: <org>/<repo> exists" - skip to Step 8 |
| **404** | Not found - proceed to Step 6 |
| **401/403** | Permission issue - warn, proceed to Step 6 |

### Step 6: Confirm Organization (only if validation failed)

Use AskUserQuestion:
- Question: "Repository not found. Is '<detected-org>' the correct organization?"
- Header: "Organization"
- Options:
  - "Yes, that's correct"
  - "No, let me specify"

### Step 7: Confirm Repository (only if validation failed)

Use AskUserQuestion:
- Question: "Is '<detected-repo-name>' the correct repository?"
- Header: "Repository"
- Options:
  - "Yes, that's correct"
  - "No, let me specify"

**After corrections, re-validate via API (Step 5).**

### Step 8: Create/Update .env

```bash
echo "GITEA_ORG=<ORG_NAME>" >> .env
echo "GITEA_REPO=<REPO_NAME>" >> .env
```

### Step 9: Optional PR Review Settings

Use AskUserQuestion:
- Question: "Configure PR review settings?"
- Header: "Settings"
- Options:
  - "Use defaults (Recommended)"
  - "Customize settings"

If customize:
- `PR_REVIEW_CONFIDENCE_THRESHOLD` (default: 0.5)
- `PR_REVIEW_AUTO_SUBMIT` (default: false)

---

## Complete

```
╔══════════════════════════════════════════════════════════════╗
║                   PROJECT CONFIGURED                         ║
╠══════════════════════════════════════════════════════════════╣
║ Organization:  <ORG_NAME>                                    ║
║ Repository:    <REPO_NAME>                                   ║
║ Config file:   ./.env                                        ║
╚══════════════════════════════════════════════════════════════╝

Ready to review PRs:
• /pr-review <number>   - Full multi-agent review
• /pr-summary <number>  - Quick summary
• /pr-findings <number> - List findings
```
