# /git-config - Configure git-flow

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔀 GIT-FLOW · Configuration                                      │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the configuration.

## Purpose

Configure git-flow settings for the current project.

## Behavior

### Interactive Configuration

```
git-flow Configuration
═══════════════════════════════════════════

Current settings:
  GIT_WORKFLOW_STYLE: feature-branch
  GIT_DEFAULT_BASE: development
  GIT_AUTO_DELETE_MERGED: true
  GIT_AUTO_PUSH: false

What would you like to configure?
1. Workflow style
2. Default base branch
3. Auto-delete merged branches
4. Auto-push after commit
5. Protected branches
6. View all settings
7. Reset to defaults
```

### Setting: Workflow Style

```
Choose your workflow style:

1. simple
   - Direct commits to development
   - No feature branches required
   - Good for solo projects

2. feature-branch (Recommended)
   - Feature branches from development
   - Merge when complete
   - Good for small teams

3. pr-required
   - Feature branches from development
   - Requires PR for merge
   - Good for code review workflows

4. trunk-based
   - Short-lived branches
   - Frequent integration
   - Good for CI/CD heavy workflows
```

### Setting: Protected Branches

```
Protected branches (comma-separated):
Current: main, master, development, staging, production

These branches will:
- Never be auto-deleted
- Require confirmation before direct commits
- Warn before force push
```

## Environment Variables

| Variable | Default | Options |
|----------|---------|---------|
| `GIT_WORKFLOW_STYLE` | `feature-branch` | simple, feature-branch, pr-required, trunk-based |
| `GIT_DEFAULT_BASE` | `development` | Any branch name |
| `GIT_AUTO_DELETE_MERGED` | `true` | true, false |
| `GIT_AUTO_PUSH` | `false` | true, false |
| `GIT_PROTECTED_BRANCHES` | `main,master,development,staging,production` | Comma-separated |
| `GIT_COMMIT_STYLE` | `conventional` | conventional, simple, detailed |
| `GIT_CO_AUTHOR` | `true` | true, false |

## Storage

Settings are stored in:
- Project: `.env` or `.claude/settings.json`
- User: `~/.config/claude/git-flow.env`

Project settings override user settings.

## Output

After configuration:
```
Configuration saved!

GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true

These settings will be used for all git-flow commands.
```
