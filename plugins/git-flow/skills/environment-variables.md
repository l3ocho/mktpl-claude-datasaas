# Environment Variables

## Purpose

Centralized reference for all git-flow environment variables and their defaults.

## When to Use

- Configuring git-flow behavior in `/git-config`
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
| `GIT_AUTO_DELETE_MERGED` | `true` | Auto-delete merged branches |
| `GIT_AUTO_DELETE_REMOTE` | `false` | Auto-delete remote branches |
| `GIT_CLEANUP_STALE` | `true` | Include stale branches in cleanup |

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

Project settings override user settings.

## Example Configuration

**.env file:**
```bash
GIT_DEFAULT_BASE=main
GIT_WORKFLOW_STYLE=pr-required
GIT_AUTO_DELETE_MERGED=true
GIT_COMMIT_STYLE=conventional
GIT_PROTECTED_BRANCHES=main,staging,production
```

## Related Skills

- skills/git-safety.md
- skills/commit-conventions.md
