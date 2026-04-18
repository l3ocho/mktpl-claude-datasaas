# Environment Variables

## Purpose

Centralized reference for all git-flow environment variables and their defaults. Also defines the mandatory load order for any git-flow command that depends on these variables.

## Load Order Rule (ENFORCED)

**This skill MUST be loaded as the first operational step of any git-flow command that references environment variables.**

Every git-flow command that lists this skill in its `## Skills` section MUST include an explicit **Step 0: Load Environment** in its workflow, executed before any git operation, API call, or user prompt. The Step 0 procedure is:

1. Read project `.env` if present. Parse all `GIT_*` and `GITEA_*` variables.
2. Read user config (`~/.config/claude/git-flow.env`) if present.
3. Apply precedence: **project `.env` > user config > defaults in this skill**.
4. Expose resolved values for use in subsequent steps.
5. If any variable required by later steps is missing and has no default, halt and ask the user — do NOT guess.

**Rationale:** Skills are declarative — listing a skill in a command's `## Skills` section declares the skill is relevant, not that it has already been executed. Load order must be made explicit in the command's workflow steps; otherwise the LLM may defer env-var loading until after an operation has already failed or produced incorrect results.

**This rule applies to all six executable git-flow commands:** `gitflow-commit`, `gitflow-branch-start`, `gitflow-branch-cleanup`, `gitflow-status`, `gitflow-config`, `gitflow-setup`. The router command `gitflow.md` is exempt (it only routes to sub-commands, which each apply this rule independently).

## When to Use

- Step 0 of any git-flow command that reads env vars
- Configuring git-flow behavior in `/gitflow config`
- Documenting available options to users
- Setting up project-specific overrides

## Core Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_DEFAULT_BASE` | `development` | Base branch for new branches and merges |
| `GIT_PROTECTED_BRANCHES` | `main,master,development,staging,production` | Comma-separated list of protected branches |
| `GIT_WORKFLOW_STYLE` | `feature-branch` | Workflow: simple, feature-branch, pr-required, trunk-based |

## Commit Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_COMMIT_STYLE` | `conventional` | Message style: conventional, simple, detailed |
| `GIT_SIGN_COMMITS` | `false` | Use GPG signing |
| `GIT_CO_AUTHOR` | `true` | Include Claude co-author footer |

## Push/Sync Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_AUTO_PUSH` | `false` | Auto-push after commit |
| `GIT_PUSH_STRATEGY` | `rebase` | Handle diverged branches: rebase, merge |
| `GIT_SYNC_STRATEGY` | `rebase` | Incorporate upstream changes: rebase, merge |
| `GIT_AUTO_PRUNE` | `true` | Auto-prune stale remote refs on sync |

## Branch Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIT_BRANCH_PREFIX` | `true` | Use type/ prefix for branches |
| `GIT_AUTO_DELETE_MERGED` | `true` | Auto-invoke cleanup of merged branches after merge (NOT silent force-delete authorization — see git-safety.md) |
| `GIT_AUTO_DELETE_REMOTE` | `false` | Include remote deletion in cleanup by default |
| `GIT_CLEANUP_STALE` | `true` | Include stale branches in cleanup |

## Gitea Integration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GITEA_API_URL` | (none) | Gitea API endpoint. Signals where Gitea lives. **Does NOT signal "use API for branch deletion"** — no `delete_branch` MCP tool exists; use `git push --delete` for remote cleanup. |
| `GITEA_API_TOKEN` | (none) | Gitea personal access token |
| `GITEA_REPO` | (auto-detect from `git remote -v`) | `owner/repo` format for project mode |

## Workflow Styles

### simple
- Direct commits to main/development
- No feature branches required
- Best for: Solo projects, small scripts

### feature-branch (Default)
- Feature branches from development
- Merge when complete
- Best for: Small teams

### pr-required
- Feature branches from development
- Requires PR for merge
- Best for: Code review workflows

### trunk-based
- Short-lived branches (< 1 day)
- Frequent integration
- Best for: CI/CD heavy workflows

## Storage Locations

| Scope | Location | Priority |
|-------|----------|----------|
| Project | `.env` or `.claude/settings.json` | Highest |
| User | `~/.config/claude/git-flow.env` | Lower |

Project settings override user settings. Both override defaults in this skill.

## Example Configuration

**Project `.env`:**
```bash
GIT_DEFAULT_BASE=main
GIT_WORKFLOW_STYLE=pr-required
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_DELETE_REMOTE=true
GIT_COMMIT_STYLE=conventional
GIT_PROTECTED_BRANCHES=main,staging,production
GITEA_API_URL=https://gitea.hotserv.cloud/api/v1
```

## Related Skills

- skills/git-safety.md
- skills/commit-conventions.md
