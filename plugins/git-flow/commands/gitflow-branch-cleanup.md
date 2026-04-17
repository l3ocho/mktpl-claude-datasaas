---
name: gitflow branch-cleanup
description: Remove merged and stale branches locally and optionally on remote
agent: git-assistant
---

# /gitflow branch-cleanup - Clean Merged and Stale Branches

## Skills

- skills/visual-header.md
- skills/git-safety.md
- skills/sync-workflow.md
- skills/environment-variables.md

## Purpose

Remove branches that have been merged OR whose remote tracking branch no longer exists.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--dry-run` | Preview without deleting |
| `--remote` | Also delete remote branches |
| `--stale-only` | Only delete stale branches (upstream gone) |

## Workflow

### Step 0: Load Environment (MANDATORY — must run before any git or API operation)

**Imperative:** Before executing any subsequent step, read environment variables per `skills/environment-variables.md`. This step is non-skippable.

1. Read project `.env` if present. Parse all `GIT_*` and `GITEA_*` variables.
2. Read user `~/.config/claude/git-flow.env` if present. Project values override user values.
3. Apply defaults from `skills/environment-variables.md` for any unset variable.
4. Expose resolved values for use in subsequent steps. Specifically for this command:
   - `GIT_PROTECTED_BRANCHES` — comma-separated list used in Step 5.
   - `GIT_DEFAULT_BASE` — base branch passed to `git branch --merged` in Step 3.
   - `GIT_AUTO_DELETE_REMOTE` — if `true` and user confirms "all", include remote deletion; informational only, does not override user selection in Step 7.
   - `GITEA_API_URL` — logged for debugging only. **Do NOT use for branch deletion** (see §5.2 of this command; no Gitea MCP `delete_branch` tool exists).
5. If `GIT_DEFAULT_BASE` is unset and no default can be inferred, halt and ask the user which base branch to use.

**Do not proceed to Step 1 until all environment variables above have been resolved.**

### Step 1: Display Header

Show the GIT-FLOW Branch Cleanup header per `skills/visual-header.md`.

### Step 2: Prune Remote Refs

Execute: `git fetch --prune`

### Step 3: Find Merged Branches

Execute: `git branch --merged <GIT_DEFAULT_BASE>`

Exclude the current branch and any branch in `GIT_PROTECTED_BRANCHES` from the result.

### Step 4: Find Stale Branches

Execute: `git branch -vv | grep ': gone]'`

This identifies local branches whose upstream remote no longer exists.

### Step 5: Exclude Protected

Per `skills/git-safety.md`, remove any branch in `GIT_PROTECTED_BRANCHES` from both the merged and stale lists. Protected branches are NEVER deleted regardless of their apparent status.

### Step 6: Present Findings

Display three clearly-labeled lists:

```
Merged branches (safe to delete with -d):
  - feat/old-feature-a
  - fix/bug-123

Stale branches (upstream gone — may contain unmerged work):
  - feat/abandoned-prototype
  - feat/spike-experiment

Protected (excluded from cleanup):
  - main
  - development
  - staging
```

If both merged and stale lists are empty: report "Nothing to clean up." and exit successfully. Do not proceed to Step 7.

### Step 7: Await User Confirmation (BLOCKING — do not proceed without user response)

**Imperative:** This step is a hard gate. You MUST invoke `AskUserQuestion` with the options below. You MUST NOT proceed to Step 8 until the user has selected one of the options via the tool.

**Fallback clause:** If `AskUserQuestion` is not available in the current transport, present the options as a numbered list in plain text AND explicitly state: "Halting. Awaiting user selection. I will not delete any branch until you reply with one of: all, merged only, stale only, pick, cancel." Then stop output and wait for the user's next message.

**Do not rationalize skipping this step.** Even if `GIT_AUTO_DELETE_MERGED=true` is set, this flag does NOT authorize bypassing confirmation. The flag only affects the default pre-selection in the prompt; the user must still confirm.

**AskUserQuestion invocation:**

- Question: "Which branches should be deleted?"
- Options:
  - `all` — delete all listed merged and stale branches
  - `merged only` — delete only merged branches (skip stale)
  - `stale only` — delete only stale branches (skip merged)
  - `pick` — interactively select specific branches to delete
  - `cancel` — abort cleanup, delete nothing

If the user selects `cancel`: exit with "Cleanup aborted by user. No branches deleted." and stop. Do not proceed to Step 8.

If the user selects `pick`: enumerate each branch and ask per-branch yes/no via a second `AskUserQuestion` invocation. Aggregate the selections before proceeding.

### Step 8a: Execute Local Cleanup

For each branch selected for deletion, apply the following procedure **in order**. Per-branch behavior depends on its category (merged vs. stale):

**For MERGED branches (strict `-d` only):**

1. Execute: `git branch -d <branch>`
2. If this succeeds, record "deleted" and move to the next branch.
3. If this FAILS (exit code non-zero): **do NOT retry with `-D`.** Instead, report the failure to the user:
   ```
   Could not delete merged branch '<branch>' with -d:
   <stderr from git>

   This is unexpected — the branch was listed as merged. Possible causes:
   - The merge base has changed since Step 3
   - The branch has commits that are merged but not reachable from <GIT_DEFAULT_BASE>

   Aborting cleanup of this branch. You may investigate manually with:
     git log <GIT_DEFAULT_BASE>..<branch>
   ```
   Continue with the next branch. Do not force-delete. Do not ask about force-deleting.

**For STALE branches (`-d` first, then escalate with user confirmation):**

1. Execute: `git branch -d <branch>`
2. If this succeeds, record "deleted" and move to the next branch.
3. If this FAILS: the branch has unmerged commits. Do NOT proceed silently. Capture the unmerged commit list:
   ```
   git log <branch> --not --branches --not --remotes
   ```
4. Invoke `AskUserQuestion` (with text-prompt fallback per Step 7) showing:
   ```
   Stale branch '<branch>' has unmerged commits:
     <abbreviated commit list, max 10>

   Force-delete with -D?
   ```
   Options: `yes` (force-delete this branch), `no` (skip this branch), `cancel all` (abort remaining deletions).
5. If user says `yes`: execute `git branch -D <branch>`. Record "force-deleted (user-confirmed)".
6. If user says `no`: skip this branch. Continue with next.
7. If user says `cancel all`: abort all remaining deletions. Report what was already done.

**Under no circumstances execute `git branch -D` without an explicit `yes` from the user for that specific branch.** The marketplace autonomous-first posture does NOT authorize silent force-deletion.

### Step 8b: Execute Remote Cleanup (only if `--remote` flag OR `GIT_AUTO_DELETE_REMOTE=true` AND user selected `all`)

**Rationale for using `git push --delete`:** There is no `delete_branch` tool in the Gitea MCP server (`mcp-gitea-pypi`). Remote branch deletion for post-hoc cleanup has no API-layer alternative. The presence of `GITEA_API_URL` signals where Gitea lives, not what mechanism to use for deletion. Future work (RFC-TBD) may add a `delete_branch` MCP tool; until then, use the git CLI against the configured remote.

For each branch that was successfully deleted locally AND has (or had) a remote tracking reference:

1. Identify the remote name (usually `origin` — detect from `git remote -v` if ambiguous).
2. Execute: `git push <remote> --delete <branch>`
3. If the remote branch was already gone (stale case), the push will fail with a "remote ref does not exist" error — this is expected and benign. Record as "already gone".
4. If the push fails for any other reason (auth, protected branch on server side, network), report the error and continue with the next branch. Do not retry automatically.

### Step 9: Report

Display a deletion summary:

```
Cleanup complete:
  Local (merged): N branches deleted
  Local (stale, force-deleted with user confirmation): M branches deleted
  Local (stale, skipped by user): K branches
  Remote: R branches deleted, S already gone
  Errors: E (see above)

Repository is tidy.
```

If `--dry-run` was used, change the header to `Dry-run complete (no changes made):` and list what WOULD have been deleted under each category, with no Step 7/8 execution.

## Output Template

```
+----------------------------------------------------------------------+
|  GIT-FLOW Branch Cleanup                                             |
+----------------------------------------------------------------------+

[Step 0 output: loaded N env vars from .env]

Merged branches: ...
Stale branches: ...
Protected (excluded): ...

[AskUserQuestion prompt — BLOCKS here]

[Deletion output]

Cleanup complete:
  Local (merged): 3 branches deleted
  Local (stale): 1 force-deleted, 1 skipped
  Remote: 3 deleted, 1 already gone
  Errors: 0

Repository is tidy.
```
