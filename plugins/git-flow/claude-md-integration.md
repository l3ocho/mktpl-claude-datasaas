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
| `/gitflow commit` | Smart commit with optional --push, --merge, --sync |
| `/gitflow commit --push` | Commit and push to remote |
| `/gitflow commit --merge` | Commit and merge into target branch |
| `/gitflow branch-start` | Start new branch |
| `/gitflow status` | Enhanced status |

### Protected Branches

Do not commit directly to: main, development, staging

---

Copy the section between the horizontal rules into your CLAUDE.md.
