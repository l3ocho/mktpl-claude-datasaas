# CLAUDE.md Git-Flow Section Template

## Purpose

Template for the Git Workflow section that `/gitflow setup` injects into a project's CLAUDE.md.

## When to Use

- During `/gitflow setup` to inject the Git Workflow section
- As reference for the expected CLAUDE.md structure

## Template

The following template uses placeholders that `/gitflow setup` replaces with actual values:

```markdown
## Git Workflow

This project uses the git-flow plugin for git operations.

### Workflow Style

**Style:** {GIT_WORKFLOW_STYLE}
**Base Branch:** {GIT_DEFAULT_BASE}

### Branch Naming

Use the format: `<type>/<description>`

Types: feat, fix, chore, docs, refactor, test, perf

Examples:
- `feat/add-user-auth`
- `fix/login-timeout`
- `chore/update-deps`

### Commit Messages

Use conventional commits:

```
<type>(<scope>): <description>

[body]

[footer]
```

### Commands

| Command | Use Case |
|---------|----------|
| `/gitflow commit` | Smart commit with optional --push, --merge, --sync |
| `/gitflow commit --push` | Commit and push to remote |
| `/gitflow commit --merge` | Commit and merge into target branch |
| `/gitflow branch-start` | Start new branch |
| `/gitflow status` | Enhanced status |

### Protected Branches

Do not commit directly to: {GIT_PROTECTED_BRANCHES}
```

## Placeholder Reference

| Placeholder | Source | Default |
|-------------|--------|---------|
| `{GIT_WORKFLOW_STYLE}` | Step 5 selection | `feature-branch` |
| `{GIT_DEFAULT_BASE}` | Step 5 selection | `development` |
| `{GIT_PROTECTED_BRANCHES}` | Step 5 selection | `main,staging` |
