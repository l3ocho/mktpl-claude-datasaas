---
name: gitflow setup
description: Configure git-flow for the current project — auto-detects Gitea config
agent: git-assistant
---

# /gitflow setup - Git-Flow Configuration

## Skills

- skills/visual-header.md
- skills/environment-variables.md
- skills/workflow-patterns/branching-strategies.md
- skills/claude-md-integration.md

## Purpose

Configure git-flow for a project. Auto-detects existing Gitea system configuration
and injects the git-flow section into the project's CLAUDE.md.

**Important:** Uses Bash, Read, Write tools only — NOT MCP tools.

## Workflow

### Step 1: Display Header

```
+----------------------------------------------------------------------+
|  GIT-FLOW Setup                                                       |
+----------------------------------------------------------------------+
```

### Step 2: Detect Gitea System Config

Check for existing Gitea configuration:

1. Read `~/.config/claude/gitea.env`
   - If found: parse GITEA_API_URL and GITEA_API_TOKEN (show URL, mask token)
   - If missing: inform user and redirect — "Run `/projman setup --full` first to configure Gitea, then come back."

### Step 3: Detect Git Repository

1. Run `git remote -v` to get remote URL
2. Parse org/repo from remote URL
3. If no git remote: warn and ask for manual GITEA_REPO value
4. If multiple git remotes: ask which to use (prefer "origin")

### Step 4: Detect Existing Configuration

Check for existing git-flow settings:

1. Read project `.env` — check for GIT_WORKFLOW_STYLE, GIT_DEFAULT_BASE
2. Read CLAUDE.md — check for "## Git Workflow" section
3. If both exist and match: "Already configured. Reconfigure? (y/n)"

### Step 5: Configure Workflow Settings

Prompt for (with defaults from `skills/environment-variables.md`):

| Setting | Default | Options |
|---------|---------|---------|
| Workflow style | feature-branch | simple, feature-branch, pr-required, trunk-based |
| Default base branch | development | main, development, custom |
| Auto-push after commit | false | true, false |
| Auto-delete merged branches | true | true, false |
| Protected branches | main,staging | comma-separated list |

Save to project `.env` (append or update existing git-flow section):

```bash
# git-flow configuration
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_PUSH=false
GIT_AUTO_DELETE_MERGED=true
GIT_PROTECTED_BRANCHES=main,staging
```

### Step 6: Inject CLAUDE.md Section

Read the project's CLAUDE.md. If a "## Git Workflow" section exists, replace it.
If not, append before the last section.

Use the template from `skills/claude-md-integration.md`, customizing with settings from Step 5:
- Replace workflow style, base branch, and protected branches with actual values
- Keep branch naming and commit message conventions as-is

### Step 7: Validate and Confirm

1. Verify `.env` was written correctly
2. Verify CLAUDE.md section was injected
3. Display summary:

```
Setup complete!

Gitea: {GITEA_API_URL} (detected from system config)
Repo: {org}/{repo} (detected from git remote)
Style: {GIT_WORKFLOW_STYLE}
Base: {GIT_DEFAULT_BASE}
Protected: {GIT_PROTECTED_BRANCHES}

CLAUDE.md updated with git-flow configuration.
```

## Edge Cases

- No CLAUDE.md in project root: Create one with just the Git Workflow section
- CLAUDE.md is read-only: Warn and output the section for manual paste
- No git remote: Skip Gitea detection, still configure workflow settings
- No Gitea system config: Warn but proceed with workflow setup (Gitea is optional)
