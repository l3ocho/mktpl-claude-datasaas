# Configuration Guide

Centralized configuration documentation for all plugins and MCP servers in the Leo Claude Marketplace.

---

## Quick Start

**After installing the marketplace and plugins via Claude Code:**

```
/setup
```

The interactive wizard auto-detects what's needed and handles everything except manually adding your API tokens.

---

## Setup Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FIRST TIME SETUP                                  │
│                         (once per machine)                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                              /setup --full
                          (or /setup auto-detects)
                                    │
     ┌──────────────────────────────┼──────────────────────────────┐
     ▼                              ▼                              ▼
┌─────────────┐            ┌─────────────────┐            ┌─────────────────┐
│  PHASE 1    │            │    PHASE 2      │            │    PHASE 3      │
│  Automated  │───────────▶│    Automated    │───────────▶│   Interactive   │
│             │            │                 │            │                 │
│ • Check     │            │ • Find MCP path │            │ • Ask Gitea URL │
│   Python    │            │ • Create venv   │            │ • Ask Org name  │
│   version   │            │ • Install deps  │            │ • Create config │
└─────────────┘            └─────────────────┘            └─────────────────┘
                                                                   │
                                                                   ▼
                                                   ┌───────────────────────────┐
                                                   │        PHASE 4            │
                                                   │     USER ACTION           │
                                                   │                           │
                                                   │  Edit config file to add  │
                                                   │  API token (for security) │
                                                   │                           │
                                                   │  nano ~/.config/claude/   │
                                                   │       gitea.env           │
                                                   └───────────────────────────┘
                                                                   │
                                                                   ▼
     ┌──────────────────────────────┬──────────────────────────────┐
     ▼                              ▼                              ▼
┌─────────────┐            ┌─────────────────┐            ┌─────────────────┐
│  PHASE 5    │            │    PHASE 6      │            │    PHASE 7      │
│ Interactive │            │    Automated    │            │    Automated    │
│             │            │                 │            │                 │
│ • Confirm   │            │ • Create .env   │            │ • Test API      │
│   repo name │            │ • Check         │            │ • Show summary  │
│   from git  │            │   .gitignore    │            │ • Restart note  │
└─────────────┘            └─────────────────┘            └─────────────────┘
                                                                   │
                                                                   ▼
                                                   ┌───────────────────────────┐
                                                   │      RESTART SESSION      │
                                                   │                           │
                                                   │  MCP tools available      │
                                                   │  after restart            │
                                                   └───────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          NEW PROJECT SETUP                                  │
│                        (once per project)                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
             /setup --quick                     /setup
             (explicit mode)               (auto-detects mode)
                    │                               │
                    │                    ┌──────────┴──────────┐
                    │                    ▼                     ▼
                    │              "Quick setup"         "Full setup"
                    │               (skips to              (re-runs
                    │              project config)          everything)
                    │                    │                     │
                    └────────────────────┴─────────────────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   PROJECT CONFIG    │
                              │                     │
                              │ • Detect repo from  │
                              │   git remote        │
                              │ • Confirm with user │
                              │ • Create .env       │
                              │ • Check .gitignore  │
                              └─────────────────────┘
                                         │
                                         ▼
                                      Done!
```

---

## What Runs Automatically vs User Interaction

### `/setup --full` - Full Setup

| Phase | Type | What Happens |
|-------|------|--------------|
| **1. Environment Check** | Automated | Verifies Python 3.10+ is installed |
| **2. MCP Server Setup** | Automated | Finds plugin path, creates venv, installs dependencies |
| **3. System Config Creation** | Interactive | Asks for Gitea URL and organization name |
| **4. Token Entry** | **User Action** | User manually edits config file to add API token |
| **5. Project Detection** | Interactive | Shows detected repo name, asks for confirmation |
| **6. Project Config** | Automated | Creates `.env` file, checks `.gitignore` |
| **7. Validation** | Automated | Tests API connectivity, shows summary |

### `/setup --quick` - Quick Project Setup

| Phase | Type | What Happens |
|-------|------|--------------|
| **1. Pre-flight Check** | Automated | Verifies system config exists |
| **2. Project Detection** | Interactive | Shows detected repo name, asks for confirmation |
| **3. Project Config** | Automated | Creates/updates `.env` file |
| **4. Gitignore Check** | Interactive | Asks to add `.env` to `.gitignore` if missing |

---

## One Command, Three Modes

| Mode | When to Use | What It Does |
|------|-------------|--------------|
| `/setup` | Any time | Auto-detects: runs full, quick, or sync as needed |
| `/setup --full` | First time on a machine | Full setup: MCP server + system config + project config |
| `/setup --quick` | Starting a new project | Quick setup: project config only (assumes system is ready) |
| `/setup --sync` | After repo move/rename | Updates .env to match current git remote |

**Auto-detection logic:**
1. No system config → **full** mode
2. System config exists, no project config → **quick** mode
3. Both exist, git remote differs → **sync** mode
4. Both exist, match → already configured, offer to reconfigure

**Typical workflow:**
1. Install plugin → run `/setup` (auto-runs full mode)
2. Start new project → run `/setup` (auto-runs quick mode)
3. Repository moved? → run `/setup` (auto-runs sync mode)

---

## Configuration Architecture

This marketplace uses a **hybrid configuration** approach:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM-LEVEL (once per machine)             │
│                    ~/.config/claude/                            │
├─────────────────────────────────────────────────────────────────┤
│  gitea.env     │  GITEA_API_URL, GITEA_API_TOKEN                       │
│  netbox.env    │  NETBOX_API_URL, NETBOX_API_TOKEN                     │
│  git-flow.env  │  GIT_WORKFLOW_STYLE, GIT_DEFAULT_BASE, etc.   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Shared across all projects
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PROJECT-LEVEL (once per project)              │
│                  <project-root>/.env                            │
├─────────────────────────────────────────────────────────────────┤
│  GITEA_REPO              │  Repository as owner/repo format    │
│  GIT_WORKFLOW_STYLE      │  (optional) Override system default │
│  PR_REVIEW_*             │  (optional) PR review settings      │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Single token per service (update once, use everywhere)
- Easy multi-project setup (just run `/setup` in each project)
- Security (tokens never committed to git, never typed into AI chat)
- Project isolation (each project can override defaults)

---

## Prerequisites

Before running `/setup`:

1. **Python 3.10+** installed
   ```bash
   python3 --version  # Should be 3.10.0 or higher
   ```

2. **Git repository** initialized (for project setup)
   ```bash
   git status  # Should show initialized repository
   ```

3. **Claude Code** installed and working with the marketplace

---

## Setup Methods

### Method 1: Interactive Wizard (Recommended)

Run the setup wizard in Claude Code:

```
/setup
```

The wizard will guide you through each step interactively and auto-detect the appropriate mode.

**Note:** After first-time setup, you'll need to restart your Claude Code session for MCP tools to become available.

### Method 2: Manual Setup

If you prefer to set up manually or need to troubleshoot:

#### Step 1: MCP Server Setup

```bash
# Navigate to marketplace directory
cd /path/to/leo-claude-mktplace

# Set up Gitea MCP server
cd mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

# (Optional) Set up NetBox MCP server
cd ../netbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

#### Step 2: System Configuration

```bash
mkdir -p ~/.config/claude

# Gitea configuration (credentials only)
cat > ~/.config/claude/gitea.env << 'EOF'
GITEA_API_URL=https://gitea.example.com
GITEA_API_TOKEN=your_token_here
EOF
chmod 600 ~/.config/claude/gitea.env
```

#### Step 3: Project Configuration

In each project root:

```bash
cat > .env << 'EOF'
GITEA_REPO=your-organization/your-repo-name
EOF
```

Add `.env` to `.gitignore` if not already there.

### Method 3: Automation Script (CI/Scripting)

For automated setups or CI environments:

```bash
cd /path/to/leo-claude-mktplace
./scripts/setup.sh
```

This script is useful for CI/CD pipelines and bulk provisioning.

---

## Configuration Reference

### System-Level Files

Located in `~/.config/claude/`:

| File | Required By | Purpose |
|------|-------------|---------|
| `gitea.env` | projman, pr-review | Gitea API credentials |
| `netbox.env` | cmdb-assistant | NetBox API credentials |
| `git-flow.env` | git-flow | Default git workflow settings |

### Gitea Configuration

```bash
# ~/.config/claude/gitea.env
GITEA_API_URL=https://gitea.example.com/api/v1
GITEA_API_TOKEN=your_gitea_token_here
```

| Variable | Description | Example |
|----------|-------------|---------|
| `GITEA_API_URL` | Gitea API endpoint (with `/api/v1`) | `https://gitea.example.com/api/v1` |
| `GITEA_API_TOKEN` | Personal access token | `abc123...` |

**Note:** `GITEA_REPO` is configured at the project level in `owner/repo` format since different projects may belong to different organizations.

**Generating a Gitea Token:**
1. Log into Gitea → **User Icon** → **Settings**
2. **Applications** tab → **Manage Access Tokens**
3. **Generate New Token** with permissions:
   - `repo` (all sub-permissions)
   - `read:org`
   - `read:user`
   - `write:repo` (for wiki access)
4. Copy token immediately (shown only once)

### NetBox Configuration

```bash
# ~/.config/claude/netbox.env
NETBOX_API_URL=https://netbox.example.com
NETBOX_API_TOKEN=your_netbox_token_here
```

| Variable | Description | Example |
|----------|-------------|---------|
| `NETBOX_API_URL` | NetBox base URL | `https://netbox.example.com` |
| `NETBOX_API_TOKEN` | API token | `abc123...` |

### Git-Flow Configuration

```bash
# ~/.config/claude/git-flow.env
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=false
GIT_PROTECTED_BRANCHES=main,master,development,staging,production
GIT_COMMIT_STYLE=conventional
GIT_CO_AUTHOR=true
```

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_WORKFLOW_STYLE` | `feature-branch` | Branching strategy |
| `GIT_DEFAULT_BASE` | `development` | Default base branch |
| `GIT_AUTO_DELETE_MERGED` | `true` | Delete merged branches |
| `GIT_AUTO_PUSH` | `false` | Auto-push after commit |
| `GIT_PROTECTED_BRANCHES` | `main,master,...` | Protected branches |
| `GIT_COMMIT_STYLE` | `conventional` | Commit message style |
| `GIT_CO_AUTHOR` | `true` | Include Claude co-author |

---

## Project-Level Configuration

Create `.env` in each project root:

```bash
# Required for projman, pr-review (use owner/repo format)
GITEA_REPO=your-organization/your-repo-name

# Optional: Override git-flow defaults
GIT_WORKFLOW_STYLE=pr-required
GIT_DEFAULT_BASE=main

# Optional: PR review settings
PR_REVIEW_CONFIDENCE_THRESHOLD=0.5
PR_REVIEW_AUTO_SUBMIT=false
```

| Variable | Required | Description |
|----------|----------|-------------|
| `GITEA_REPO` | Yes | Repository in `owner/repo` format (e.g., `my-org/my-repo`) |
| `GIT_WORKFLOW_STYLE` | No | Override system default |
| `PR_REVIEW_*` | No | PR review settings |

---

## Plugin Configuration Summary

| Plugin | System Config | Project Config | Setup Command |
|--------|---------------|----------------|---------------|
| **projman** | gitea.env | .env (GITEA_REPO=owner/repo) | `/setup` |
| **pr-review** | gitea.env | .env (GITEA_REPO=owner/repo) | `/initial-setup` |
| **git-flow** | git-flow.env (optional) | .env (optional) | None needed |
| **clarity-assist** | None | None | None needed |
| **cmdb-assistant** | netbox.env | None | `/initial-setup` |
| **data-platform** | postgres.env | .env (optional) | `/initial-setup` |
| **viz-platform** | None | .env (optional DMC_VERSION) | `/initial-setup` |
| **doc-guardian** | None | None | None needed |
| **code-sentinel** | None | None | None needed |
| **project-hygiene** | None | None | None needed |
| **claude-config-maintainer** | None | None | None needed |
| **contract-validator** | None | None | `/initial-setup` |

---

## Multi-Project Workflow

Once system-level config is set up, adding new projects is simple:

```
cd ~/projects/new-project
/setup
```

The command auto-detects that system config exists and runs quick project setup.

---

## Installing Plugins to Consumer Projects

The marketplace provides scripts to install plugins into consumer projects. This sets up the MCP server connections and adds CLAUDE.md integration snippets.

### Install a Plugin

```bash
cd /path/to/leo-claude-mktplace
./scripts/install-plugin.sh <plugin-name> <target-project-path>
```

**Examples:**
```bash
# Install data-platform to a portfolio project
./scripts/install-plugin.sh data-platform ~/projects/personal-portfolio

# Install multiple plugins
./scripts/install-plugin.sh viz-platform ~/projects/personal-portfolio
./scripts/install-plugin.sh projman ~/projects/personal-portfolio
```

**What it does:**
1. Validates the plugin exists in the marketplace
2. Adds MCP server entry to target's `.mcp.json` (if plugin has MCP server)
3. Appends integration snippet to target's `CLAUDE.md`
4. Reports changes and lists available commands

**After installation:** Restart your Claude Code session for MCP tools to become available.

### Uninstall a Plugin

```bash
./scripts/uninstall-plugin.sh <plugin-name> <target-project-path>
```

Removes the MCP server entry and CLAUDE.md integration section.

### List Installed Plugins

```bash
./scripts/list-installed.sh <target-project-path>
```

Shows which marketplace plugins are installed, partially installed, or available.

**Output example:**
```
✓ Fully Installed:
  PLUGIN                   VERSION    DESCRIPTION
  ------                   -------    -----------
  data-platform            1.3.0      pandas, PostgreSQL, and dbt integration...
  viz-platform             1.1.0      DMC validation, Plotly charts, and theming...

○ Available (not installed):
  projman                  3.4.0      Sprint planning and project management...
```

### Plugins with MCP Servers

Not all plugins have MCP servers. The install script handles this automatically:

| Plugin | Has MCP Server | Notes |
|--------|---------------|-------|
| data-platform | ✓ | pandas, PostgreSQL, dbt tools |
| viz-platform | ✓ | DMC validation, chart, theme tools |
| contract-validator | ✓ | Plugin compatibility validation |
| cmdb-assistant | ✓ (via netbox) | NetBox CMDB tools |
| projman | ✓ (via gitea) | Issue, wiki, PR tools |
| pr-review | ✓ (via gitea) | PR review tools |
| git-flow | ✗ | Commands only |
| doc-guardian | ✗ | Commands and hooks only |
| code-sentinel | ✗ | Commands and hooks only |
| clarity-assist | ✗ | Commands only |

### Script Requirements

- **jq** must be installed (`sudo apt install jq`)
- Scripts are idempotent (safe to run multiple times)

---

## Agent Frontmatter Configuration

Agents specify their configuration in frontmatter using Claude Code's supported fields. Reference: https://code.claude.com/docs/en/sub-agents

### Supported Frontmatter Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | Yes | — | Unique identifier, lowercase + hyphens |
| `description` | Yes | — | When Claude should delegate to this subagent |
| `model` | No | `inherit` | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default` | Controls permission prompts: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `disallowedTools` | No | none | Comma-separated tools to remove from agent's toolset |
| `skills` | No | none | Comma-separated skills auto-injected into context at startup |
| `hooks` | No | none | Lifecycle hooks scoped to this subagent |

### Complete Agent Matrix

| Plugin | Agent | `model` | `permissionMode` | `disallowedTools` | `skills` |
|--------|-------|---------|-------------------|--------------------|----------|
| projman | planner | opus | default | — | frontmatter (2) + body text (12) |
| projman | orchestrator | sonnet | acceptEdits | — | frontmatter (2) + body text (10) |
| projman | executor | sonnet | bypassPermissions | — | frontmatter (7) |
| projman | code-reviewer | opus | default | Write, Edit, MultiEdit | frontmatter (4) |
| pr-review | coordinator | sonnet | plan | Write, Edit, MultiEdit | — |
| pr-review | security-reviewer | sonnet | plan | Write, Edit, MultiEdit | — |
| pr-review | performance-analyst | sonnet | plan | Write, Edit, MultiEdit | — |
| pr-review | maintainability-auditor | haiku | plan | Write, Edit, MultiEdit | — |
| pr-review | test-validator | haiku | plan | Write, Edit, MultiEdit | — |
| data-platform | data-advisor | sonnet | default | — | — |
| data-platform | data-analysis | sonnet | plan | Write, Edit, MultiEdit | — |
| data-platform | data-ingestion | haiku | acceptEdits | — | — |
| viz-platform | design-reviewer | sonnet | plan | Write, Edit, MultiEdit | — |
| viz-platform | layout-builder | sonnet | default | — | — |
| viz-platform | component-check | haiku | plan | Write, Edit, MultiEdit | — |
| viz-platform | theme-setup | haiku | acceptEdits | — | — |
| contract-validator | full-validation | sonnet | default | — | — |
| contract-validator | agent-check | haiku | plan | Write, Edit, MultiEdit | — |
| code-sentinel | security-reviewer | sonnet | plan | Write, Edit, MultiEdit | — |
| code-sentinel | refactor-advisor | sonnet | acceptEdits | — | — |
| doc-guardian | doc-analyzer | sonnet | acceptEdits | — | — |
| clarity-assist | clarity-coach | sonnet | default | Write, Edit, MultiEdit | — |
| git-flow | git-assistant | haiku | acceptEdits | — | — |
| claude-config-maintainer | maintainer | sonnet | acceptEdits | — | frontmatter (2) |
| cmdb-assistant | cmdb-assistant | sonnet | default | — | — |

### Design Principles

- `bypassPermissions` is granted to exactly ONE agent (Executor) which has code-sentinel PreToolUse hook + Code Reviewer downstream as safety nets.
- `plan` mode is assigned to all pure analysis agents (pr-review, read-only validators).
- `disallowedTools: Write, Edit, MultiEdit` provides defense-in-depth on agents that should never write files.
- `skills` frontmatter is used for agents with ≤7 skills where guaranteed loading is safety-critical. Agents with 8+ skills use body text `## Skills to Load` for selective loading.
- `hooks` (agent-scoped) is reserved for future use (v6.0+).

Override any field by editing the agent's `.md` file in `plugins/{plugin}/agents/`.

### permissionMode Guide

| Value | Prompts for file ops? | Prompts for Bash? | Prompts for MCP? | Use when |
|-------|-----------------------|-------------------|-------------------|----------|
| `default` | Yes | Yes | No (MCP bypasses permissions) | You want full visibility |
| `acceptEdits` | No | Yes | No | Core job is file read/write, Bash visibility useful |
| `dontAsk` | No | No (most) | No | Even Bash prompts are friction |
| `bypassPermissions` | No | No | No | Agent has downstream safety layers |
| `plan` | N/A (read-only) | N/A (read-only) | No | Pure analysis, no modifications |

### disallowedTools Guide

Use `disallowedTools` to remove specific tools from an agent's toolset. This is a blacklist — the agent inherits all tools from the main thread, then the listed tools are removed.

Prefer `disallowedTools` over `tools` (whitelist) because:
- New MCP servers are automatically available without updating every agent.
- Less configuration to maintain.
- Easier to audit — you only list what's blocked.

Common patterns:
- `disallowedTools: Write, Edit, MultiEdit` — read-only agent, cannot modify files.
- `disallowedTools: Bash` — no shell access (rare, most agents need at least read-only Bash).

### skills Frontmatter Guide

The `skills` field auto-injects skill file contents into the agent's context window at startup. The agent does NOT need to read the files — they are already present.

**When to use frontmatter `skills`:**
- Agent has ≤7 skills.
- Skills are safety-critical (e.g., `branch-security`, `runaway-detection`).
- You need guaranteed loading — no risk of the agent skipping a skill.

**When to keep body text `## Skills to Load`:**
- Agent has 8+ skills (context window cost too high for full injection).
- Skills are situational — not all needed for every invocation.
- Agent benefits from selective loading based on the specific task.

Skill names in frontmatter are resolved relative to the plugin's `skills/` directory. Use the filename without the `.md` extension.

### Phase-Based Skill Loading (Body Text)

For agents with 8+ skills, use **phase-based loading** in the agent body text. This structures skill reads into logical phases, with explicit instructions to read each skill exactly once.

**Pattern:**

```markdown
## Skill Loading Protocol

**Frontmatter skills (auto-injected, always available — DO NOT re-read these):**
- `skill-a` — description
- `skill-b` — description

**Phase 1 skills — read ONCE at session start:**
- skills/validation-skill.md
- skills/safety-skill.md

**Phase 2 skills — read ONCE when entering main work:**
- skills/workflow-skill.md
- skills/domain-skill.md

**CRITICAL: Read each skill file exactly ONCE. Do NOT re-read skill files between MCP API calls.**
```

**Benefits:**
- Frontmatter skills (always needed) are auto-injected — zero file read cost
- Phase skills are read once at the appropriate time — not re-read per API call
- `batch-execution` skill provides protocol for API-heavy phases
- ~76-83% reduction in skill-related token consumption for typical sprints

**Currently applied to:**
- Planner agent: 2 frontmatter + 12 body text (3 phases)
- Orchestrator agent: 2 frontmatter + 10 body text (2 phases)

---

## Automatic Validation Features

### API Validation

When running `/setup`, the command:

1. **Detects** organization and repository from git remote URL
2. **Validates** via Gitea API: `GET /api/v1/repos/{org}/{repo}`
3. **Auto-fills** if repository exists and is accessible (no confirmation needed)
4. **Asks for confirmation** only if validation fails (404 or permission error)

This catches typos and permission issues before saving configuration.

### Mismatch Detection (SessionStart Hook)

When you start a Claude Code session, a hook automatically:

1. Reads `GITEA_REPO` (in `owner/repo` format) from `.env`
2. Compares with current `git remote get-url origin`
3. **Warns** if mismatch detected: "Repository location mismatch. Run `/setup --sync` to update."

This helps when you:
- Move a repository to a different organization
- Rename a repository
- Clone a repo but forget to update `.env`

---

## Verification

### Test Gitea Connection

```bash
source ~/.config/claude/gitea.env
curl -H "Authorization: token $GITEA_API_TOKEN" "$GITEA_API_URL/user"
```

### Verify Project Setup

In Claude Code, after restarting your session:
```
/labels-sync
```

If this works, your setup is complete.

---

## Troubleshooting

### MCP tools not available

**Cause:** Session wasn't restarted after setup.
**Solution:** Exit Claude Code and start a new session.

### "Configuration not found" error

```bash
# Check system config exists
ls -la ~/.config/claude/gitea.env

# Check permissions (should be 600)
stat ~/.config/claude/gitea.env
```

### Authentication failed

```bash
# Test token directly
source ~/.config/claude/gitea.env
curl -H "Authorization: token $GITEA_API_TOKEN" "$GITEA_API_URL/user"
```

If you get 401, regenerate your token in Gitea.

### MCP server won't start

```bash
# Check venv exists
ls /path/to/mcp-servers/gitea/.venv

# If missing, create venv (do NOT delete existing venvs)
cd /path/to/mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Wrong repository

```bash
# Check project .env
cat .env

# Verify GITEA_REPO is in owner/repo format and matches Gitea exactly
# Example: GITEA_REPO=my-org/my-repo
```

---

## Security Best Practices

1. **Never commit tokens**
   - Keep credentials in `~/.config/claude/` only
   - Add `.env` to `.gitignore`

2. **Secure configuration files**
   ```bash
   chmod 600 ~/.config/claude/*.env
   ```

3. **Never type tokens into AI chat**
   - Always edit config files directly in your editor
   - The `/setup` wizard respects this

4. **Rotate tokens periodically**
   - Every 6-12 months
   - Immediately if compromised

5. **Minimum permissions**
   - Only grant required token permissions
   - Use separate tokens for different environments
