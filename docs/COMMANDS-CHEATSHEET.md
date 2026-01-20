# Plugin Commands Cheat Sheet

Quick reference for all commands in the Claude Code Marketplace.

---

## Command Reference Table

| Plugin | Command | Auto | Manual | Description |
|--------|---------|:----:|:------:|-------------|
| **projman** | `/sprint-plan` | | X | Start sprint planning with AI-guided architecture analysis and issue creation |
| **projman** | `/sprint-start` | | X | Begin sprint execution with dependency analysis and parallel task coordination |
| **projman** | `/sprint-status` | | X | Check current sprint progress and identify blockers |
| **projman** | `/review` | | X | Pre-sprint-close code quality review (debug artifacts, security, error handling) |
| **projman** | `/test-check` | | X | Run tests and verify coverage before sprint close |
| **projman** | `/sprint-close` | | X | Complete sprint and capture lessons learned to Gitea Wiki |
| **projman** | `/labels-sync` | | X | Synchronize label taxonomy from Gitea |
| **projman** | `/initial-setup` | | X | Run installation script for projman plugin setup |
| **projman** | `/test-gen` | | X | Generate comprehensive tests for specified code |
| **git-flow** | `/commit` | | X | Create commit with auto-generated conventional message |
| **git-flow** | `/commit-push` | | X | Commit and push to remote in one operation |
| **git-flow** | `/commit-merge` | | X | Commit current changes, then merge into target branch |
| **git-flow** | `/commit-sync` | | X | Full sync: commit, push, and sync with upstream/base branch |
| **git-flow** | `/branch-start` | | X | Create new feature/fix/chore branch with naming conventions |
| **git-flow** | `/branch-cleanup` | | X | Remove merged branches locally and optionally on remote |
| **git-flow** | `/git-status` | | X | Enhanced git status with recommendations |
| **git-flow** | `/git-config` | | X | Configure git-flow settings for the project |
| **pr-review** | `/pr-review` | | X | Full multi-agent PR review with confidence scoring |
| **pr-review** | `/pr-summary` | | X | Quick summary of PR changes |
| **pr-review** | `/pr-findings` | | X | List and filter review findings by category/severity |
| **clarity-assist** | `/clarify` | | X | Full 4-D prompt optimization with ND accommodations |
| **clarity-assist** | `/quick-clarify` | | X | Rapid single-pass clarification for simple requests |
| **doc-guardian** | `/doc-audit` | | X | Full documentation audit - scans for doc drift |
| **doc-guardian** | `/doc-sync` | | X | Synchronize pending documentation updates |
| **doc-guardian** | *PostToolUse hook* | X | | Silently detects doc drift on Write/Edit |
| **doc-guardian** | *Stop hook* | X | | Offers to sync docs at session end |
| **code-sentinel** | `/security-scan` | | X | Full security audit (SQL injection, XSS, secrets, etc.) |
| **code-sentinel** | `/refactor` | | X | Apply refactoring patterns to improve code |
| **code-sentinel** | `/refactor-dry` | | X | Preview refactoring without applying changes |
| **code-sentinel** | *PreToolUse hook* | X | | Scans code before writing; blocks critical issues |
| **claude-config-maintainer** | `/config-analyze` | | X | Analyze CLAUDE.md for optimization opportunities |
| **claude-config-maintainer** | `/config-optimize` | | X | Optimize CLAUDE.md structure with preview/backup |
| **claude-config-maintainer** | `/config-init` | | X | Initialize new CLAUDE.md for a project |
| **cmdb-assistant** | `/cmdb-search` | | X | Search NetBox for devices, IPs, sites |
| **cmdb-assistant** | `/cmdb-device` | | X | Manage network devices (create, view, update, delete) |
| **cmdb-assistant** | `/cmdb-ip` | | X | Manage IP addresses and prefixes |
| **cmdb-assistant** | `/cmdb-site` | | X | Manage sites, locations, racks, and regions |
| **project-hygiene** | *PostToolUse hook* | X | | Removes temp files, warns about unexpected root files |

---

## Plugins by Category

| Category | Plugins | Primary Use |
|----------|---------|-------------|
| **Task Planning** | projman, clarity-assist | Sprint management, requirement clarification |
| **Code Quality** | code-sentinel, pr-review | Security scanning, PR reviews |
| **Documentation** | doc-guardian, claude-config-maintainer | Doc sync, CLAUDE.md maintenance |
| **Git Operations** | git-flow | Commits, branches, workflow automation |
| **Infrastructure** | cmdb-assistant | NetBox CMDB management |
| **Maintenance** | project-hygiene | Automatic cleanup |

---

## Hook-Based Automation Summary

| Plugin | Hook Event | Behavior |
|--------|------------|----------|
| **doc-guardian** | PostToolUse (Write/Edit) | Silently tracks documentation drift |
| **doc-guardian** | Stop | Prompts to sync if drift detected |
| **code-sentinel** | PreToolUse (Write/Edit) | Scans for security issues; blocks critical vulnerabilities |
| **project-hygiene** | PostToolUse (Write/Edit) | Cleans temp files, warns about misplaced files |

---

## Dev Workflow Examples

### Example 1: Starting a New Feature Sprint

A typical workflow for planning and executing a feature sprint:

```
1. /clarify                  # Clarify requirements if vague
2. /sprint-plan              # Plan the sprint with architecture analysis
3. /labels-sync              # Ensure labels are up-to-date
4. /sprint-start             # Begin execution with dependency ordering
5. /branch-start feat/...    # Create feature branch
   ... implement features ...
6. /commit                   # Commit with conventional message
7. /sprint-status            # Check progress mid-sprint
8. /review                   # Pre-close quality review
9. /test-check               # Verify test coverage
10. /sprint-close            # Capture lessons learned
```

### Example 2: Daily Development Cycle

Quick daily workflow with git-flow:

```
1. /git-status               # Check current state
2. /branch-start fix/...     # Start bugfix branch
   ... make changes ...
3. /commit                   # Auto-generate commit message
4. /commit-push              # Push to remote
5. /branch-cleanup           # Clean merged branches
```

### Example 3: Pull Request Review Workflow

Reviewing a PR before merge:

```
1. /pr-summary               # Quick overview of changes
2. /pr-review                # Full multi-agent review
3. /pr-findings              # Filter findings by severity
4. /security-scan            # Deep security audit if needed
```

### Example 4: Documentation Maintenance

Keeping docs in sync:

```
1. /doc-audit                # Scan for documentation drift
2. /doc-sync                 # Apply pending updates
3. /config-analyze           # Check CLAUDE.md health
4. /config-optimize          # Optimize if needed
```

### Example 5: Code Refactoring Session

Safe refactoring with preview:

```
1. /refactor-dry             # Preview opportunities
2. /security-scan            # Baseline security check
3. /refactor                 # Apply improvements
4. /test-check               # Verify nothing broke
5. /commit                   # Commit with descriptive message
```

### Example 6: Infrastructure Documentation

Managing infrastructure with CMDB:

```
1. /cmdb-search "server"     # Find existing devices
2. /cmdb-device view X       # Check device details
3. /cmdb-ip list             # List available IPs
4. /cmdb-site view Y         # Check site info
```

### Example 7: New Project Setup

Setting up a project with marketplace plugins:

```
1. /config-init              # Create CLAUDE.md
2. /initial-setup            # Setup projman (if using)
3. /labels-sync              # Sync Gitea labels
4. /sprint-plan              # Plan first sprint
```

---

## Quick Tips

- **Hooks run automatically** - doc-guardian and code-sentinel protect you without manual invocation
- **Use `/commit` over `git commit`** - generates better commit messages following conventions
- **Run `/review` before `/sprint-close`** - catches issues before closing the sprint
- **Use `/clarify` for vague requests** - especially helpful for complex requirements
- **`/refactor-dry` is safe** - always preview before applying refactoring changes

---

## MCP Server Requirements

Some plugins require MCP server connectivity:

| Plugin | MCP Server | Purpose |
|--------|------------|---------|
| projman | Gitea | Issues, PRs, wiki, labels, milestones |
| pr-review | Gitea | PR operations and reviews |
| cmdb-assistant | NetBox | Infrastructure CMDB |

Ensure credentials are configured in `~/.config/claude/gitea.env` or `~/.config/claude/netbox.env`.

---

*Last Updated: 2026-01-20*
