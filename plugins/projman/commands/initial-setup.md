---
description: Interactive setup wizard for projman plugin - configures MCP servers, credentials, and project settings
---

# Initial Setup Wizard

This command guides the user through complete projman setup interactively. It handles both first-time marketplace setup and per-project configuration.

## Important Context

- **This command uses Bash, Read, Write, and AskUserQuestion tools** - NOT MCP tools
- **MCP tools won't work until after setup + session restart**
- **Tokens must be entered manually by the user** for security (not typed into chat)

---

## Quick Path Detection

**FIRST**, check if system-level setup is already complete:

```bash
cat ~/.config/claude/gitea.env 2>/dev/null | grep -v "^#" | grep -v "PASTE_YOUR" | grep -v "example.com" | grep "GITEA_TOKEN=" && echo "SYSTEM_CONFIGURED" || echo "SYSTEM_NEEDS_SETUP"
```

**If SYSTEM_CONFIGURED:**

The system-level configuration already exists. Offer the user a choice:

Use AskUserQuestion:
- Question: "System configuration found. What would you like to do?"
- Header: "Setup Mode"
- Options:
  - "Quick project setup only (Recommended for new projects)"
  - "Full setup (re-check everything)"

**If "Quick project setup":**
- Skip directly to **Phase 4: Project-Level Configuration**
- This is equivalent to running `/project-init`

**If "Full setup":**
- Continue with Phase 1 below

**If SYSTEM_NEEDS_SETUP:**
- Continue with Phase 1 (full setup required)

---

## Phase 1: Environment Validation

### Step 1.1: Check Python Version

Run this command to verify Python 3.10+ is available:

```bash
python3 --version
```

**If version is below 3.10:**
- Stop setup and inform user: "Python 3.10 or higher is required. Please install it and run /initial-setup again."
- Provide installation hints based on OS (apt, brew, etc.)

**If successful:** Continue to next step.

---

## Phase 2: MCP Server Setup

### Step 2.1: Locate the Plugin Installation

The plugin is installed somewhere on the system. Find the MCP server directory by resolving the path.

First, identify where this plugin is installed. The MCP server should be accessible via the symlink structure. Look for the gitea MCP server:

```bash
# Find the plugin's mcp-servers directory (search common locations)
find ~/.claude ~/.config/claude -name "mcp_server" -path "*gitea*" 2>/dev/null | head -5
```

If found, extract the parent path (the gitea MCP server root).

**Alternative:** If the user knows the marketplace location, ask them:

Use AskUserQuestion:
- Question: "Where is the Leo Claude Marketplace installed?"
- Options:
  - "~/.claude/plugins/leo-claude-mktplace" (default Claude plugins location)
  - "Let me find it automatically"
  - Other (user provides path)

### Step 2.2: Check if Virtual Environment Exists

Once you have the MCP server path (e.g., `/path/to/mcp-servers/gitea`), check for the venv:

```bash
ls -la /path/to/mcp-servers/gitea/.venv/bin/python 2>/dev/null && echo "VENV_EXISTS" || echo "VENV_MISSING"
```

### Step 2.3: Create Virtual Environment (if missing)

If venv doesn't exist:

```bash
cd /path/to/mcp-servers/gitea && python3 -m venv .venv
```

Then install dependencies:

```bash
cd /path/to/mcp-servers/gitea && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && deactivate
```

**If pip install fails:**
- Show the error to the user
- Suggest: "Check your internet connection and try again. You can also manually run: `cd /path/to/mcp-servers/gitea && source .venv/bin/activate && pip install -r requirements.txt`"

### Step 2.4: NetBox MCP Server (Optional)

Check if the user wants to set up the NetBox MCP server (for cmdb-assistant plugin):

Use AskUserQuestion:
- Question: "Do you want to set up the NetBox MCP server for infrastructure management?"
- Options:
  - "Yes, set up NetBox MCP"
  - "No, skip NetBox (Recommended if not using cmdb-assistant)"

If yes, repeat steps 2.2-2.3 for `/path/to/mcp-servers/netbox`.

---

## Phase 3: System-Level Configuration

System configuration is stored in `~/.config/claude/` and contains credentials that work across all projects.

### Step 3.1: Create Config Directory

```bash
mkdir -p ~/.config/claude
```

### Step 3.2: Check Gitea Configuration

```bash
cat ~/.config/claude/gitea.env 2>/dev/null || echo "FILE_NOT_FOUND"
```

**If file doesn't exist:** Go to Step 3.3 (Create Template)
**If file exists:** Read it and check if values are placeholders (contain "example.com" or "your_" or "token_here"). If placeholders, go to Step 3.4 (Update Existing).
**If file has real values:** Go to Step 3.5 (Validate).

### Step 3.3: Create Gitea Configuration Template

Gather the Gitea server URL from the user.

Use AskUserQuestion:
- Question: "What is your Gitea server URL? (e.g., https://gitea.company.com)"
- Header: "Gitea URL"
- Options:
  - "https://gitea.hotserv.cloud" (if this is Leo's setup)
  - "Other (I'll provide the URL)"

If "Other", ask the user to type the URL.

Now create the configuration file with a placeholder for the token:

```bash
cat > ~/.config/claude/gitea.env << 'EOF'
# Gitea API Configuration
# Generated by /initial-setup
# Note: GITEA_ORG is configured per-project in .env

GITEA_URL=<USER_PROVIDED_URL>
GITEA_TOKEN=PASTE_YOUR_TOKEN_HERE
EOF
chmod 600 ~/.config/claude/gitea.env
```

Replace `<USER_PROVIDED_URL>` with the actual value from the user.

### Step 3.4: Token Entry Instructions

**CRITICAL: Do not ask the user to type the token into chat.**

Display these instructions clearly:

---

**Action Required: Add Your Gitea API Token**

I've created the configuration file at `~/.config/claude/gitea.env` but you need to add your API token manually for security.

**Steps:**
1. Open the file in your editor:
   ```
   nano ~/.config/claude/gitea.env
   ```
   Or use any editor you prefer.

2. Generate a Gitea token (if you don't have one):
   - Go to your Gitea instance → User Icon → Settings
   - Click "Applications" tab
   - Under "Manage Access Tokens", click "Generate New Token"
   - Name it something like "claude-code"
   - Select permissions: `repo` (all), `read:org`, `read:user`
   - Click "Generate Token" and copy it immediately

3. Replace `PASTE_YOUR_TOKEN_HERE` with your actual token

4. Save the file

---

Use AskUserQuestion:
- Question: "Have you added your Gitea token to ~/.config/claude/gitea.env?"
- Header: "Token Added?"
- Options:
  - "Yes, I've added the token"
  - "I need help generating a token"
  - "Skip for now (I'll do it later)"

**If "I need help":** Provide detailed instructions for their specific Gitea instance.
**If "Skip":** Warn that MCP tools won't work until configured, but continue with project setup.

### Step 3.5: Validate Gitea Configuration

Read the config file and verify it has non-placeholder values:

```bash
source ~/.config/claude/gitea.env && echo "URL: $GITEA_URL" && echo "TOKEN_LENGTH: ${#GITEA_TOKEN}"
```

If TOKEN_LENGTH is less than 10 or contains "PASTE" or "your_", the token hasn't been set properly.

**Note:** GITEA_ORG is configured per-project in `.env`, not in the system-level config.

**Test connectivity (optional but recommended):**

```bash
source ~/.config/claude/gitea.env && curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITEA_TOKEN" "$GITEA_URL/api/v1/user"
```

- **200:** Success! Credentials are valid.
- **401:** Invalid token.
- **404/Connection error:** Invalid URL or network issue.

Report the result to the user.

### Step 3.6: Git-Flow Configuration (Optional)

Use AskUserQuestion:
- Question: "Do you want to configure git-flow defaults for smart commits?"
- Header: "Git-Flow"
- Options:
  - "Yes, use recommended defaults (Recommended)"
  - "Yes, let me customize"
  - "No, skip git-flow configuration"

If yes with defaults:
```bash
cat > ~/.config/claude/git-flow.env << 'EOF'
# Git-Flow Default Configuration
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=false
GIT_PROTECTED_BRANCHES=main,master,development,staging,production
GIT_COMMIT_STYLE=conventional
GIT_CO_AUTHOR=true
EOF
chmod 600 ~/.config/claude/git-flow.env
```

If customize, use AskUserQuestion for each setting.

---

## Phase 4: Project-Level Configuration

Project configuration is stored in `.env` in the current project root.

### Step 4.1: Verify Current Directory

Confirm we're in the right place:

```bash
pwd && git rev-parse --show-toplevel 2>/dev/null || echo "NOT_A_GIT_REPO"
```

If not a git repo, ask the user:

Use AskUserQuestion:
- Question: "The current directory doesn't appear to be a git repository. Where should I create the project configuration?"
- Options:
  - "This directory is correct, continue anyway"
  - "Let me navigate to the right directory first"

### Step 4.2: Check Existing Project Configuration

```bash
cat .env 2>/dev/null || echo "FILE_NOT_FOUND"
```

If `.env` exists and has `GITEA_REPO=` set to a non-placeholder value, skip to Phase 5.

### Step 4.3: Infer Organization and Repository from Git Remote

Try to detect org and repo name automatically:

```bash
git remote get-url origin 2>/dev/null
```

Parse the output to extract both organization and repository:
- `git@gitea.example.com:org/repo-name.git` → org: `org`, repo: `repo-name`
- `https://gitea.example.com/org/repo-name.git` → org: `org`, repo: `repo-name`

Extract organization:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\/[^/]*$/\1/'
```

Extract repository:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\)\.git$/\1/' | sed 's/.*\/\([^/]*\)$/\1/'
```

### Step 4.4: Validate Repository via Gitea API

**Before asking for confirmation**, verify the repository exists and is accessible:

```bash
source ~/.config/claude/gitea.env
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITEA_TOKEN" "$GITEA_URL/api/v1/repos/<detected-org>/<detected-repo>"
```

**Based on response:**

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| **200** | Repository exists and accessible | **Auto-fill without asking** - skip to Step 4.7 |
| **404** | Repository not found | Ask user to confirm/correct (Step 4.5) |
| **401/403** | Token issue or no access | Warn about permissions, ask to confirm |
| **Other** | Network/server issue | Warn, ask to confirm manually |

**If 200 OK:** Display confirmation message and skip to Step 4.7:
"Verified: Repository '<detected-org>/<detected-repo>' exists and is accessible."

### Step 4.5: Confirm Organization (only if API validation failed)

Use AskUserQuestion:
- Question: "Repository '<detected-org>/<detected-repo>' was not found. Is '<detected-org>' the correct organization?"
- Header: "Organization"
- Options:
  - "Yes, that's correct"
  - "No, let me specify the correct organization"

If no, ask user to provide the correct organization name.

### Step 4.6: Confirm Repository Name (only if API validation failed)

Use AskUserQuestion:
- Question: "Is '<detected-repo-name>' the correct Gitea repository name?"
- Header: "Repository"
- Options:
  - "Yes, that's correct"
  - "No, let me specify the correct name"

If no, ask user to provide the correct name.

**After user provides corrections, re-validate via API (Step 4.4)** to ensure the corrected values are valid.

### Step 4.7: Create Project Configuration

```bash
cat > .env << 'EOF'
# Project Configuration for projman
# Generated by /initial-setup

GITEA_ORG=<ORG_NAME>
GITEA_REPO=<REPO_NAME>
EOF
```

Replace `<REPO_NAME>` with the confirmed value.

**Important:** Check if `.env` is in `.gitignore`:

```bash
grep -q "^\.env$" .gitignore 2>/dev/null && echo "GITIGNORE_OK" || echo "GITIGNORE_MISSING"
```

If not in `.gitignore`, warn the user:
"Warning: `.env` is not in your `.gitignore`. Consider adding it to prevent accidentally committing credentials."

---

## Phase 5: Final Validation and Next Steps

### Step 5.1: Summary Report

Display a summary of what was configured:

```
╔══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETE                            ║
╠══════════════════════════════════════════════════════════════╣
║ MCP Server (Gitea):     ✓ Installed                          ║
║ System Config:          ✓ ~/.config/claude/gitea.env         ║
║ Project Config:         ✓ ./.env                             ║
║ Gitea Connection:       ✓ Verified (or ⚠ Not tested)         ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 5.2: Session Restart Notice

**IMPORTANT:** Display this notice clearly:

---

**⚠️ Session Restart Required**

The MCP server has been configured but won't be available until you restart your Claude Code session.

**To complete setup:**
1. Exit this Claude Code session (type `/exit` or close the terminal)
2. Start a new Claude Code session in this project
3. The Gitea MCP tools will now be available

**After restart, you can:**
- Run `/labels-sync` to sync your label taxonomy
- Run `/sprint-plan` to start planning
- Use MCP tools like `list_issues`, `create_issue`, etc.

---

### Step 5.3: Troubleshooting Checklist

If something isn't working after restart, check:

1. **MCP server not found:** Verify venv exists at the expected path
2. **Authentication failed:** Re-check token in `~/.config/claude/gitea.env`
3. **Wrong repository:** Verify `GITEA_REPO` in `./.env` matches Gitea exactly
4. **Network error:** Ensure Gitea URL is accessible from this machine

---

## Re-Running This Command

This command is safe to run multiple times:
- Existing venvs are skipped (not recreated)
- Existing config files are checked for validity
- Only missing or placeholder values are updated
- Project config can be regenerated for new projects

---

## Quick Reference: Files Created

| File | Purpose | Contains |
|------|---------|----------|
| `~/.config/claude/gitea.env` | System credentials | URL, token, org |
| `~/.config/claude/git-flow.env` | Git defaults | Workflow settings |
| `./.env` | Project settings | Repository name |
| `<mcp-server>/.venv/` | Python environment | Dependencies |
