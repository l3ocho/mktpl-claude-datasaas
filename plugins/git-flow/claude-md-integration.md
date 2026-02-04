# git-flow - CLAUDE.md Integration

Add the following section to your project's CLAUDE.md file to enable git-flow.

---

## Git Workflow

This project uses the git-flow plugin for git operations.

### Workflow Style

**Style:** feature-branch
**Base Branch:** development

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
| `/git-commit` | Create commit with smart message |
| `/git-commit-push` | Commit and push |
| `/git-commit-merge` | Commit and merge to base |
| `/branch-start` | Start new branch |
| `/git-status` | Enhanced status |

### Protected Branches

Do not commit directly to: main, development, staging

---

Copy the section between the horizontal rules into your CLAUDE.md.
