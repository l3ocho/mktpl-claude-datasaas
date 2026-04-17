# Git Safety

## Purpose

Defines protected branches, destructive command warnings, and enforced safety checks to prevent accidental data loss.

## When to Use

- Before any commit, push, or merge operation
- When user attempts to work on protected branches
- Before executing any destructive command (delete, reset, force push)
- Loaded automatically by commands that list it in their `## Skills` section

## Protected Branches

Default protected branches (configurable via `GIT_PROTECTED_BRANCHES` environment variable):

- `main`
- `master`
- `development`
- `staging`
- `production`

## Protection Rules

| Action | Behavior |
|--------|----------|
| Direct commit on protected branch | Warn and offer to create feature branch |
| Force push to protected branch | Require explicit confirmation |
| Deletion of protected branch | BLOCKED completely — no override |
| Merge INTO protected branch | Allowed via standard workflow |

## Protected Branch Warning

When committing on a protected branch:

```
You are on a protected branch: development

Protected branches typically have push restrictions that will prevent
direct commits from being pushed to the remote.

Options:
1. Create a feature branch and continue (Recommended)
2. Continue on this branch anyway (may fail on push)
3. Cancel
```

## Destructive Commands — Enforced Rules

The following commands are **destructive**. Each has a MANDATORY pre-execution check. The check is not optional and is not bypassed by any environment variable, flag, or "autonomous mode" setting.

| Command | Risk | Required Pre-Check |
|---------|------|-------------------|
| `git push --force` | Overwrites remote history | Prefer `--force-with-lease`; require confirmation if force is unavoidable |
| `git reset --hard` | Loses uncommitted changes | Warn about unsaved work; offer `git stash` first |
| `git branch -D` | Deletes unmerged branch | See "Branch Deletion Safety — Hard Rules" below |
| `git clean -fd` | Deletes untracked files | List files first; require confirmation |

## Safe Alternatives

| Risky | Safe Alternative |
|-------|------------------|
| `git push --force` | `git push --force-with-lease` |
| `git branch -D` | `git branch -d` (merged-only safe delete) |
| `git reset --hard` | `git stash` first, then reset |
| `git checkout .` | Review changes first |

## Branch Deletion Safety — Hard Rules

**These rules are enforced. They are not guidelines.**

### Rule 1: Protected Branches Are Never Deleted

Any branch in `GIT_PROTECTED_BRANCHES` (resolved at Step 0 of the invoking command) MUST NOT be deleted — locally or remotely — under any circumstance. This includes `main`, `master`, `development`, `staging`, `production` by default. No flag, no "autonomous" mode, no user request during execution can override this.

If a user explicitly asks to delete a protected branch, respond:

```
Refusing to delete protected branch '<n>'. Protected branches are configured
via GIT_PROTECTED_BRANCHES in .env. If you genuinely need to delete this branch,
update GIT_PROTECTED_BRANCHES first, then retry.
```

### Rule 2: `-D` Is Forbidden Without Prior `-d` Failure

You MUST attempt `git branch -d <branch>` first. Only if `-d` fails AND you have surfaced the failure reason to the user AND the user has explicitly authorized force-deletion for that specific branch, may you execute `git branch -D <branch>`.

Prohibited patterns:

- Running `git branch -D` as the first deletion attempt.
- Running `git branch -D` because "I know the branch is merged".
- Running `git branch -D` in a loop without per-branch user authorization.
- Running `git branch -D` because `GIT_AUTO_DELETE_MERGED=true` is set. This flag authorizes automatic invocation of the cleanup command, not silent force-deletion.

### Rule 3: In branch-cleanup Context — Merged Branches Are `-d` Only

When invoked from `/gitflow branch-cleanup`, branches identified as merged (Step 3 output) MUST be deleted with `-d` only. If `-d` fails on a merged branch, the cleanup aborts that branch, reports the failure to the user, and moves on. It does NOT escalate to `-D`. A merged branch that won't delete with `-d` indicates inconsistent state that warrants human investigation, not force.

### Rule 4: In branch-cleanup Context — Stale Branches Follow Escalation Pattern

When invoked from `/gitflow branch-cleanup`, branches identified as stale (Step 4 output) follow this escalation:

1. Attempt `git branch -d <branch>`.
2. If success: done.
3. If failure: capture unmerged commit list via `git log <branch> --not --branches --not --remotes`.
4. Invoke `AskUserQuestion` with the commit list and options `yes` / `no` / `cancel all`.
5. If user says `yes`: execute `git branch -D <branch>`.
6. If user says `no` or `cancel all`: do not execute `-D`.

Silent `-D` in any step of this sequence is a policy violation.

### Rule 5: Force-Delete Requires Context, Not Just Authorization

When asking the user to authorize `-D`, you MUST show:

- The branch name.
- The unmerged commit list (abbreviated to max 10 entries).
- A clear binary choice (`yes`/`no`, or `yes`/`no`/`cancel all` in batch contexts).

Asking "force-delete branch X? y/n" without showing WHY force is needed (the unmerged commits) does not satisfy this rule.

## Push Rejection Handling

When push fails on a protected branch at the remote:

```
Push rejected: Remote protection rules prevent direct push to development.

Options:
1. Create a pull request instead (Recommended)
2. Review branch protection settings
3. Cancel
```

## Stale Branch Detection

Branches whose upstream remote has been deleted:

```bash
git branch -vv | grep ': gone]'
```

These are candidates for deletion but MUST follow Rule 4 above. Being "stale" is not the same as being "merged" — stale branches may contain unmerged work.

## Safety Protocols for Other Destructive Operations

### Before Any Destructive Operation

Show:
- What the operation will do.
- Current state (before).
- Expected outcome (after).
- Recovery options if the operation fails or is regretted.

### Protected Branches — UI Example

```
Cannot directly modify 'main' branch.

This branch is protected. You should:
1. Create a feature branch
2. Make your changes
3. Create a pull request

Would you like me to create a branch for this change?
```

## Related Skills

- skills/branch-naming.md
- skills/merge-workflow.md
- skills/environment-variables.md
