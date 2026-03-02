---
name: claude-config baseline
description: Save or restore the permission baseline in settings.json
---

# /claude-config baseline

Manage the permission baseline stored in `.claude/settings.json`. The baseline contains optimized permissions that persist across sessions, immune to Claude Code's session-approval overwrites.

## Skills to Load

Before executing, load:
- `skills/visual-header.md`
- `skills/settings-optimization.md`

## Visual Output

```
+-----------------------------------------------------------------+
|  CONFIG-MAINTAINER - Permission Baseline                         |
+-----------------------------------------------------------------+
```

## Usage

```
/claude-config baseline save              # Save current optimized permissions to settings.json
/claude-config baseline restore           # Reset settings.local.json to baseline-only
/claude-config baseline show              # Display current baseline contents
/claude-config baseline diff              # Show difference between baseline and current local
```

## Sub-Commands

### `save`

Writes the current optimized permission set to `.claude/settings.json`:

1. **If `/claude-config optimize-settings` was just run:** Use the optimized output as the baseline
2. **If not:** Run the audit analysis first to determine the recommended permission set
3. **Verify review layers** before writing (same as optimize-settings)
4. **Show preview** of what will be written to `settings.json`
5. **Create backup** of existing `settings.json` if it exists: `.claude/backups/settings.json.{YYYYMMDD-HHMMSS}`
6. **Write** the baseline to `.claude/settings.json`
7. **Offer to clean** `settings.local.json` — remove any patterns now covered by the baseline

Output:
```
Baseline saved to .claude/settings.json

Contents:
  allow: [XX patterns]
  deny: [X patterns]

This baseline will persist across sessions regardless of
interactive approval changes to settings.local.json.

Recommendation: Commit .claude/settings.json to version control.
```

### `restore`

Resets `settings.local.json` to contain only machine-specific patterns not in the baseline:

1. **Read baseline** from `.claude/settings.json`
2. **Read current** `settings.local.json`
3. **Compute diff** — identify patterns in local that are NOT in baseline
4. **Show preview:**
   ```
   Patterns in settings.local.json not covered by baseline:
     - Bash(conda activate *)     [machine-specific]
     - Write(/home/leo/custom/*) [machine-specific]

   These will be KEPT. All other patterns will be removed
   (they're already in the baseline).

   Remove XX redundant patterns from settings.local.json?
     [1] Yes, clean up
     [2] No, keep as-is
     [3] Remove ALL local patterns (baseline-only)
   ```
5. **Backup** before writing
6. **Write** cleaned `settings.local.json`

### `show`

Display the current baseline:

```
Current Permission Baseline (.claude/settings.json):

  allow: [list of patterns]
  deny: [list of patterns]

Last modified: YYYY-MM-DD HH:MM:SS
Committed to git: Yes/No
```

If no baseline exists, report that and suggest running `baseline save`.

### `diff`

Show what's different between the baseline and current local settings:

```
Baseline vs. Current Local Settings
====================================

In baseline but NOT in local (always active via settings.json):
  [These patterns are still in effect — no action needed]
  + Edit
  + Write
  + Bash(git *)
  ...

In local but NOT in baseline (session drift or machine-specific):
  + Bash(/home/leo/scripts/custom.sh)    [likely machine-specific]
  + Write(/tmp/test/**)                  [likely session drift]
  + Bash(pip install pandas)             [likely session approval]

Overlap (in both files — redundant in local):
  ~ Bash(grep *)    [safe to remove from local]
  ~ Bash(cat *)     [safe to remove from local]

Recommendation: Run `/claude-config baseline restore` to clean up XX redundant patterns.
```

## Safety Rules

1. **ALWAYS backup before writing** to either file
2. **ALWAYS show preview** before any modification
3. **Never modify deny rules** without explicit confirmation
4. **Never remove the baseline** — `restore` cleans local, not settings.json
5. Backups go to `.claude/backups/` with timestamps

## DO NOT

- Write to settings.json without showing preview
- Remove deny rules silently
- Delete settings.json (only overwrite with new baseline)
- Skip backup before writing
