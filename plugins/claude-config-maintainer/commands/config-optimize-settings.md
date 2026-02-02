---
name: config-optimize-settings
description: Optimize settings.local.json permissions based on audit recommendations
---

# /config-optimize-settings

Optimize Claude Code `settings.local.json` permission patterns and apply named profiles.

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
/config-optimize-settings                    # Apply audit recommendations
/config-optimize-settings --dry-run          # Preview only, no changes
/config-optimize-settings --profile=reviewed # Apply named profile
/config-optimize-settings --consolidate-only # Only merge/dedupe, no new rules
```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without applying |
| `--profile=NAME` | Apply named profile (`conservative`, `reviewed`, `autonomous`) |
| `--consolidate-only` | Only deduplicate and merge patterns, don't add new rules |
| `--no-backup` | Skip backup (not recommended) |

## Workflow

### Step 1: Run Audit Analysis

Execute the same analysis as `/config-audit-settings`:
1. Locate settings file
2. Parse permission arrays
3. Detect issues (duplicates, subsets, merge candidates, etc.)
4. Verify active review layers
5. Calculate current score

### Step 2: Generate Optimization Plan

Based on audit results, create a change plan:

**For `--consolidate-only`:**
- Remove exact duplicates
- Remove subset patterns covered by broader patterns
- Merge similar patterns (4+ threshold)
- Remove stale patterns for non-existent paths
- Remove conflicting allow entries that are already denied

**For `--profile=NAME`:**
- Calculate diff between current permissions and target profile
- Show additions and removals
- Preserve any custom deny rules not in profile

**For default (full optimization):**
- Apply all consolidation changes
- Add recommended patterns based on verified review layers
- Suggest profile alignment if appropriate

### Step 3: Show Before/After Preview

**MANDATORY:** Always show preview before applying changes.

```
Current Settings:
  allow: [12 patterns]
  deny: [4 patterns]

Proposed Changes:

  REMOVE from allow (redundant):
    - Write(plugins/projman/*) [covered by Write(plugins/**)]
    - Write(plugins/git-flow/*) [covered by Write(plugins/**)]
    - Bash(git status) [covered by Bash(git *)]

  ADD to allow (recommended):
    + Bash(npm *) [2 review layers active]
    + Bash(pytest *) [2 review layers active]

  ADD to deny (security):
    + Bash(curl * | bash*) [missing safety rule]

After Optimization:
  allow: [10 patterns]
  deny: [5 patterns]

Score Impact: 67/100 → 85/100 (+18 points)
```

### Step 4: Request User Approval

Ask for confirmation before proceeding:

```
Apply these changes to .claude/settings.local.json?
  [1] Yes, apply changes
  [2] No, cancel
  [3] Apply partial (select which changes)
```

### Step 5: Create Backup

**Before any write operation:**

```bash
# Backup location
.claude/backups/settings.local.json.{YYYYMMDD-HHMMSS}
```

Create the `.claude/backups/` directory if it doesn't exist.

### Step 6: Apply Changes

Write the optimized `settings.local.json` file.

### Step 7: Verify

Re-read the file and re-calculate the score to confirm improvement.

```
Optimization Complete!

Backup saved: .claude/backups/settings.local.json.20260202-143022

Settings Efficiency Score: 85/100 (+18 from 67)
  Redundancy:       25/25 (+8)
  Coverage:         22/25 (+5)
  Safety Alignment: 23/25 (+3)
  Profile Fit:      15/25 (+2)

Changes applied:
  - Removed 3 redundant patterns
  - Added 2 recommended patterns
  - Added 1 safety deny rule
```

## Profile Application

When using `--profile=NAME`:

### `conservative`
```
Switching to conservative profile...

This profile:
  - Allows: Read, Glob, Grep, LS, basic Bash commands
  - Allows: Write/Edit only for docs/
  - Denies: .env*, secrets/, rm -rf, sudo

All other Write/Edit operations will prompt for approval.
```

### `reviewed`
```
Switching to reviewed profile...

Prerequisites verified:
  ✓ code-sentinel hook active (PreToolUse)
  ✓ doc-guardian hook active (PostToolUse)
  ✓ 2+ review layers detected

This profile:
  - Allows: All file operations (Edit, Write, MultiEdit)
  - Allows: Scoped Bash commands (git, npm, python, etc.)
  - Denies: .env*, secrets/, rm -rf, sudo, curl|bash
```

### `autonomous`
```
⚠️  WARNING: Autonomous profile requested

This profile allows unscoped Bash execution.
Only use in fully sandboxed environments (CI, containers).

Confirm this is a sandboxed environment?
  [1] Yes, this is sandboxed - apply autonomous profile
  [2] No, cancel
```

## Safety Rules

1. **ALWAYS backup before writing** (unless `--no-backup`)
2. **NEVER remove deny rules without explicit confirmation**
3. **NEVER add unscoped `Bash` to allow** — always use scoped patterns
4. **Preview is MANDATORY** before applying changes
5. **Verify review layers** before recommending broad permissions

## Output Format

### Dry Run Output

```
+-----------------------------------------------------------------+
|  CONFIG-MAINTAINER - Settings Optimization                       |
+-----------------------------------------------------------------+

DRY RUN - No changes will be made

[... preview content ...]

To apply these changes, run:
  /config-optimize-settings
```

### Applied Output

```
+-----------------------------------------------------------------+
|  CONFIG-MAINTAINER - Settings Optimization                       |
+-----------------------------------------------------------------+

Optimization Applied Successfully

Backup: .claude/backups/settings.local.json.20260202-143022

[... summary of changes ...]

Score: 67/100 → 85/100
```

## DO NOT

- Apply changes without showing preview
- Remove deny rules silently
- Add unscoped `Bash` permission
- Skip backup without explicit `--no-backup` flag
- Apply `autonomous` profile without sandbox confirmation
- Recommend broad permissions without verifying review layers
