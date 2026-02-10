# Setup Workflows

Shared workflows for the `/projman setup` command modes.

## Mode Detection Logic

Determine setup mode automatically:

```
1. Check ~/.config/claude/gitea.env exists
   - If missing → FULL mode needed

2. If gitea.env exists, check project .env
   - If .env missing → QUICK mode (project setup)

3. If both exist, compare git remote with .env values
   - If mismatch → SYNC mode needed
   - If match → already configured, offer reconfigure option
```

## Full Setup Workflow

Complete first-time setup including MCP servers, credentials, and project.

### Phase 1: Environment Validation

```bash
# Check Python 3.10+
python3 --version  # Should be 3.10+
```

If Python < 3.10, stop and ask user to install.

### Phase 2: MCP Server Setup

1. **Locate Marketplace Installation**
   ```bash
   MKTPLACE_DIR=$(find ~/.claude/plugins/marketplaces -maxdepth 1 -name "mktpl-claude-datasaas" -type d 2>/dev/null)
   echo "Marketplace at: $MKTPLACE_DIR"
   ```
   If not found, stop — marketplace not installed.

2. **Run setup-venvs.sh**
   ```bash
   cd "$MKTPLACE_DIR" && ./scripts/setup-venvs.sh
   ```
   This handles all 5 MCP servers (gitea, netbox, data-platform, viz-platform, contract-validator):
   - Creates venvs in `~/.cache/claude-mcp-venvs/mktpl-claude-datasaas/{server}/.venv/`
   - Installs requirements and editable packages
   - Creates symlinks back to `mcp-servers/{server}/.venv`
   - Uses hash-based change detection for incremental updates

3. **Verify**
   ```bash
   cd "$MKTPLACE_DIR" && ./scripts/setup-venvs.sh --check
   ```
   All 5 servers should report OK.

4. **If setup-venvs.sh fails**, fall back to manual per-server setup:
   ```bash
   cd "$MKTPLACE_DIR/mcp-servers/gitea"
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   [ -f pyproject.toml ] && .venv/bin/pip install -e .
   ```
   Repeat for each server the user needs.

### Phase 3: System-Level Configuration

1. **Create Config Directory**
   ```bash
   mkdir -p ~/.config/claude
   ```

2. **Create gitea.env Template**
   ```env
   GITEA_API_URL=https://your-gitea-instance/api/v1
   GITEA_API_TOKEN=
   ```

3. **Token Entry (SECURITY)**
   - DO NOT ask for token in chat
   - Instruct user to edit file manually
   - Provide command: `nano ~/.config/claude/gitea.env`

4. **Validate Token**
   ```bash
   curl -s -H "Authorization: token $TOKEN" "$GITEA_API_URL/user"
   ```
   - 200 OK = valid
   - 401 = invalid token

### Phase 4: Project-Level Configuration

See **Quick Setup Workflow** below.

### Phase 5: Final Validation

Display summary:
- MCP server: ✓/✗
- System config: ✓/✗
- Project config: ✓/✗

**Important:** Session restart required for MCP tools to load.

---

## Quick Setup Workflow

Project-level setup only (assumes system config exists).

### Step 1: Verify System Config

```bash
cat ~/.config/claude/gitea.env
```

If missing or empty token, redirect to FULL mode.

### Step 2: Verify Git Repository

```bash
git rev-parse --git-dir 2>/dev/null
```

If not a git repo, stop and inform user.

### Step 3: Check Existing Config

If `.env` exists:
- Show current GITEA_ORG and GITEA_REPO
- Ask: Keep current or reconfigure?

### Step 4: Detect Org/Repo

Parse git remote URL:

```bash
git remote get-url origin
# https://gitea.example.com/org-name/repo-name.git
# → org: org-name, repo: repo-name
```

### Step 5: Validate via API

```bash
curl -s -H "Authorization: token $TOKEN" \
  "$GITEA_API_URL/repos/$ORG/$REPO"
```

- 200 OK = auto-fill without asking
- 404 = ask user to confirm/correct

### Step 6: Create .env

```env
GITEA_ORG=detected-org
GITEA_REPO=detected-repo
```

### Step 7: Check .gitignore

If `.env` not in `.gitignore`:
- Warn user about security risk
- Offer to add it

---

## Sync Workflow

Update project config when git remote changed.

### Step 1: Read Current Config

```bash
grep GITEA_ORG .env
grep GITEA_REPO .env
```

### Step 2: Detect Git Remote

Parse current remote URL (same as Quick Step 4).

### Step 3: Compare Values

| Current | Detected | Action |
|---------|----------|--------|
| Match | Match | "Already in sync" - exit |
| Different | Different | Show diff, ask to update |

### Step 4: Show Changes

```
Current:  org/old-repo
Detected: org/new-repo

Update configuration? [y/n]
```

### Step 5: Validate New Values

API check on detected org/repo.

### Step 6: Update .env

Replace GITEA_ORG and GITEA_REPO values.

### Step 7: Confirm

```
✓ Project configuration updated
  GITEA_ORG: new-org
  GITEA_REPO: new-repo
```

---

## Visual Header

All setup modes use:

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  ⚙️ SETUP                                                        ║
║  [Mode: Full | Quick | Sync]                                     ║
╚══════════════════════════════════════════════════════════════════╝
```

## DO NOT

- Ask for tokens in chat (security risk)
- Skip venv creation for MCP servers
- Create .env without checking .gitignore
- Proceed if API validation fails
