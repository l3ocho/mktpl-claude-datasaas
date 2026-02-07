---
name: gitflow commit
description: Create a git commit with auto-generated conventional commit message. Supports --push, --merge, --sync flags.
agent: git-assistant
---

# /gitflow commit - Smart Commit

## Skills

- skills/visual-header.md
- skills/git-safety.md
- skills/commit-conventions.md
- skills/sync-workflow.md
- skills/merge-workflow.md
- skills/environment-variables.md

## Purpose

Create a git commit with an auto-generated conventional commit message. Optionally push, merge, or sync in the same operation.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--message`, `-m` | Override auto-generated message |
| `--all`, `-a` | Stage all changes before commit |
| `--push` | After commit: push to remote (replaces former `/git-commit-push`) |
| `--merge [target]` | After commit: merge into target branch (replaces former `/git-commit-merge`) |
| `--sync` | After commit: push and sync with base branch (replaces former `/git-commit-sync`) |
| `--force` | Force push (with --push or --sync, requires confirmation) |
| `--squash` | Squash commits on merge (with --merge) |
| `--no-delete` | Keep branch after merge (with --merge) |
| `--base` | Override default base branch (with --sync) |
| `--no-rebase` | Use merge instead of rebase (with --sync) |

## Workflow

### Base: Commit
1. **Display header** — GIT-FLOW Smart Commit
2. **Check protected branch** — per git-safety.md
3. **Analyze changes** — `git status` and `git diff --staged`
4. **Handle unstaged** — Prompt to stage if nothing staged
5. **Generate message** — Create conventional commit (per commit-conventions.md)
6. **Confirm or edit** — Present message with options
7. **Execute commit**

### Flag: --push
8. **Check upstream** — Set up tracking if needed
9. **Push to remote**
10. **Handle conflicts** — Offer rebase/merge/force if push fails

### Flag: --merge
8. **Identify target** — Prompt for target branch if not specified
9. **Select strategy** — Merge commit, squash, or rebase (per merge-workflow.md)
10. **Execute merge** — Switch to target, pull, merge, push
11. **Handle conflicts** — Guide resolution
12. **Cleanup** — Offer to delete merged branch

### Flag: --sync
8. **Push committed changes**
9. **Fetch with prune** — `git fetch --all --prune`
10. **Sync with base** — Rebase on base branch (per sync-workflow.md)
11. **Handle conflicts** — Guide resolution (per merge-workflow.md)
12. **Push again** — `git push --force-with-lease` if rebased
13. **Report stale branches**

## Flag Mutual Exclusivity

`--push`, `--merge`, and `--sync` are mutually exclusive. If multiple are provided, error with:
"Only one of --push, --merge, or --sync may be specified."

## Output

### Base commit:
```
Committed: abc1234
feat(auth): add password reset functionality
```

### With --push:
```
Committed: abc1234
Pushed to: origin/feat/password-reset
```

### With --merge:
```
Committed: abc1234
Merged feat/password-reset -> development
```

### With --sync:
```
Committed: abc1234
Pushed to: origin/feat/password-reset
Synced with: development
```
