---
name: claude-config optimize-settings
description: Write autonomous permissions to settings.json. Claude Code will not prompt for any approvals except .venv deletion.
---

# /claude-config optimize-settings

Write autonomous permissions to `.claude/settings.json`. Claude Code will not prompt for any approvals except `.venv` deletion. Marketplace hooks (code-sentinel, git-flow) are the actual safety layer.

## Skills to Load

Before executing, load:
- `skills/visual-header.md`
- `skills/settings-optimization.md`
- `skills/pre-change-protocol.md`

## Visual Output

```
+-----------------------------------------------------------------+
|  CONFIG-MAINTAINER - Settings Optimization                       |
+-----------------------------------------------------------------+
```

## Usage

```
/claude-config optimize-settings                         # Write autonomous config to settings.json (default)
/claude-config optimize-settings --dry-run               # Preview the JSON that would be written
/claude-config optimize-settings --profile=reviewed      # Legacy: write reviewed profile instead
/claude-config optimize-settings --profile=conservative  # Legacy: write conservative profile
/claude-config optimize-settings --target=local          # Write to settings.local.json (with warning)
/claude-config optimize-settings --no-backup             # Skip backup
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview the JSON that would be written, no changes applied |
| `--profile=NAME` | Write a legacy named profile (`conservative`, `reviewed`) instead of autonomous config |
| `--target=local` | Write to `settings.local.json` instead of `settings.json` — warns this file gets overwritten by session approvals |
| `--no-backup` | Skip backup (not recommended) |

## Default Workflow (No Flags — Autonomous Config)

### Step 1: Read Existing Settings

Read `.claude/settings.json` if it exists:
- Note any custom `deny` rules the user has added — these will be preserved
- Note the existing `allow` rules — these will be replaced by the autonomous config

If `.claude/settings.json` does not exist, skip to Step 3.

### Step 2: Backup

**Before any write operation:**

```bash
# Backup location
.claude/backups/settings.json.{YYYYMMDD-HHMMSS}
```

Create the `.claude/backups/` directory if it doesn't exist. Skip if `--no-backup`.

### Step 3: Write Autonomous Config

Write the following to `.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "WebFetch(*)",
      "WebSearch",
      "mcp__*"
    ],
    "deny": [
      "Bash(rm -rf .venv)",
      "Bash(rm -r .venv)",
      "Bash(rm -rf .venv/)",
      "Bash(rm -r .venv/)"
    ]
  }
}
```

**Merge deny rules:** If the user had custom `deny` rules in the existing file that are NOT already in the above deny list, append them to the deny array.

### Step 4: Offer settings.local.json Cleanup (Optional)

If `.claude/settings.local.json` exists:

```
settings.local.json detected.

The autonomous config in settings.json now covers all operations.
Patterns in settings.local.json that duplicate settings.json are redundant.

Clean up redundant patterns from settings.local.json?
  [1] Yes, remove patterns already covered by autonomous config
  [2] No, leave settings.local.json as-is
  [3] Skip this — I'll clean it manually later
```

**Note:** This cleanup is optional and does not affect the autonomous config that was just written.

### Step 5: Confirm

Display what was written:

```
Autonomous Config Written

Target:  .claude/settings.json
Backup:  .claude/backups/settings.json.20260331-143022

Permissions written:
  defaultMode: bypassPermissions
  allow: Bash(*), Read(*), Write(*), Edit(*), WebFetch(*), WebSearch, mcp__*
  deny:  .venv deletion guards (4 rules)
  [+ N custom deny rules preserved]

Claude Code will NOT prompt for approval on any operation except .venv deletion.
Marketplace hooks (code-sentinel, git-flow) remain the active safety layer.
```

## Legacy Profile Workflow (`--profile=NAME`)

When using `--profile=reviewed` or `--profile=conservative`, the command applies the named profile from the settings-optimization skill instead of the autonomous config. These profiles use granular pattern-matching and are documented in the skill's **Legacy Profiles** section.

### Prerequisites Check (for `--profile=reviewed`)

```
Switching to reviewed profile...

Prerequisites verified:
  ✓ code-sentinel hook active (PreToolUse)
  ✓ git-flow hook active (PreToolUse)
  ✓ 2+ review layers detected
```

### Before/After Preview

**MANDATORY for `--profile` workflows:** Show preview before applying.

```
Current Settings:
  allow: [12 patterns]
  deny: [4 patterns]

Proposed Changes:

  REMOVE from allow (redundant):
    - Write(plugins/projman/*) [covered by Write(plugins/**)]
    - Bash(git status) [covered by Bash(git *)]

  ADD to allow (recommended):
    + Bash(npm *) [2 review layers active]

  ADD to deny (security):
    + Bash(curl * | bash*) [missing safety rule]

After Optimization:
  allow: [10 patterns]
  deny: [5 patterns]
```

### Profile Application

**`--profile=conservative`:**
```
This profile:
  - Allows: Read, Glob, Grep, LS, basic Bash commands
  - Allows: Write/Edit only for docs/
  - Denies: .env*, secrets/, rm -rf, sudo

All other Write/Edit operations will prompt for approval.
```

**`--profile=reviewed`:**
```
This profile:
  - Allows: All file operations (Edit, Write, MultiEdit)
  - Allows: Scoped Bash commands (git, npm, python, etc.)
  - Denies: .env*, secrets/, rm -rf, sudo, curl|bash
```

## Dry Run Output

```
+-----------------------------------------------------------------+
|  CONFIG-MAINTAINER - Settings Optimization                       |
+-----------------------------------------------------------------+

DRY RUN - No changes will be made

Would write to: .claude/settings.json

{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": ["Bash(*)", "Read(*)", "Write(*)", "Edit(*)", "WebFetch(*)", "WebSearch", "mcp__*"],
    "deny": ["Bash(rm -rf .venv)", "Bash(rm -r .venv)", "Bash(rm -rf .venv/)", "Bash(rm -r .venv/)"]
  }
}

To apply, run:
  /claude-config optimize-settings
```

## `--target=local` Warning

```
⚠️  WARNING: --target=local specified

Writing to settings.local.json. This file is overwritten by Claude Code
session approvals during interactive use. Your optimized config may be
lost the next time Claude Code writes to this file.

Recommended: Write to settings.json instead (default behavior).

Continue with settings.local.json?
  [1] Yes, write to settings.local.json
  [2] No, write to settings.json instead (recommended)
```

## Safety Rules

1. **ALWAYS backup before writing** (unless `--no-backup`)
2. **NEVER remove user's existing deny rules** — always merge them into the deny array
3. **Default target is settings.json** — not settings.local.json
4. **Dry run shows exact JSON** that would be written
5. **--target=local always warns** about session-approval overwrite risk

## DO NOT

- Remove deny rules silently
- Write to settings.local.json without `--target=local` flag and warning
- Skip backup without explicit `--no-backup` flag
- Show scoring or profile analysis as part of the default (no-flag) workflow
