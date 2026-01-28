# git-flow

Git workflow automation with intelligent commit messages and branch management.

## Overview

git-flow streamlines common git operations with smart defaults, conventional commit messages, and workflow enforcement. It supports multiple branching strategies and adapts to your team's workflow.

## Commands

| Command | Description |
|---------|-------------|
| `/commit` | Create commit with auto-generated conventional message (with protected branch detection) |
| `/commit-push` | Commit and push in one operation |
| `/commit-merge` | Commit and merge into target branch |
| `/commit-sync` | Full sync: commit, push, and rebase on base branch |
| `/branch-start` | Start new feature/fix/chore branch |
| `/branch-cleanup` | Clean up merged branches |
| `/git-status` | Enhanced status with recommendations |
| `/git-config` | Configure git-flow settings |

## Workflow Styles

| Style | Description | Best For |
|-------|-------------|----------|
| `simple` | Direct commits to main | Solo projects |
| `feature-branch` | Feature branches, merge when done | Small teams |
| `pr-required` | All changes via pull request | Code review workflows |
| `trunk-based` | Short-lived branches, frequent integration | CI/CD heavy |

## Installation

Add to your project's `.claude/settings.json`:

```json
{
  "plugins": ["git-flow"]
}
```

## Configuration

Set environment variables in `.env` or `~/.config/claude/git-flow.env`:

```bash
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=false
GIT_PROTECTED_BRANCHES=main,master,development,staging
GIT_COMMIT_STYLE=conventional
GIT_CO_AUTHOR=true
```

Or use `/git-config` for interactive configuration.

## Features

### Smart Commit Messages

Analyzes staged changes to generate appropriate conventional commit messages:

```
feat(auth): add password reset functionality

Implement forgot password flow with email verification.
Includes rate limiting and token expiration.
```

### Branch Naming

Enforces consistent branch naming:

```
feat/add-user-authentication
fix/login-timeout-error
chore/update-dependencies
```

### Safety Checks

- **Protected branch detection**: Before committing, checks if you're on a protected branch (main, master, development, staging, production by default). Offers to create a feature branch automatically instead of committing directly to protected branches.
- Confirms force push operations
- Prevents accidental branch deletion

### Conflict Resolution

The git-assistant agent helps resolve merge conflicts with analysis and recommendations.

## Usage Examples

### Start a Feature

```
/branch-start add user authentication

→ Created: feat/add-user-authentication
  Based on: development
```

### Commit Changes

```
/commit

→ Analyzing changes...
→ Proposed: feat(auth): add login component
→ Committed: abc1234
```

### Full Sync

```
/commit-sync

→ Committed: abc1234
→ Pushed to origin
→ Rebased on development
→ Status: Clean, up-to-date
```

## Documentation

- [Branching Strategy Guide](docs/BRANCHING-STRATEGY.md) - Detailed documentation of the `development -> staging -> main` promotion flow

## Integration

For CLAUDE.md integration instructions, see `claude-md-integration.md`.

## License

MIT
