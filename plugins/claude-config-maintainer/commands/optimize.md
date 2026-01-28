---
description: Optimize CLAUDE.md structure and content
---

# Optimize CLAUDE.md

This command automatically optimizes your project's CLAUDE.md file based on best practices and identified issues.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚙️ CONFIG-MAINTAINER · CLAUDE.md Optimization                   │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the optimization.

## What This Command Does

1. **Analyze Current File** - Identifies all optimization opportunities
2. **Plan Changes** - Determines what to restructure, condense, or add
3. **Show Preview** - Displays before/after comparison
4. **Apply Changes** - Updates the file with your approval
5. **Verify Results** - Confirms improvements achieved

## Usage

```
/config-optimize
```

Or specify specific optimizations:

```
/config-optimize --condense        # Focus on reducing verbosity
/config-optimize --restructure     # Focus on reorganization
/config-optimize --add-missing     # Focus on adding missing sections
```

## Optimization Actions

### Restructure
- Reorder sections by importance
- Group related content together
- Improve header hierarchy
- Add navigation aids

### Condense
- Remove redundant explanations
- Convert verbose text to bullet points
- Eliminate duplicate content
- Shorten overly detailed sections

### Enhance
- Add missing essential sections
- Improve unclear instructions
- Add helpful examples
- Highlight critical rules

### Format
- Standardize header styles
- Fix code block formatting
- Align list formatting
- Improve table layouts

## Expected Output

```
CLAUDE.md Optimization
======================

Current Analysis:
- Score: 72/100
- Lines: 245
- Issues: 4

Planned Optimizations:

1. ADD: Quick Start section (new, ~15 lines)
   + Build command
   + Test command
   + Run command

2. CONDENSE: Testing section (34 → 8 lines)
   Before: Verbose explanation with redundant setup info
   After: Concise command reference with comments

3. REMOVE: Duplicate git workflow (lines 189-200)
   Keeping: Original at lines 102-115

4. FORMAT: Standardize headers
   Changing 12 headers from "## Title:" to "## Title"

Preview Changes? [Y/n] y

--- CLAUDE.md (before)
+++ CLAUDE.md (after)

@@ -1,5 +1,20 @@
 # CLAUDE.md

+## Quick Start
+
+```bash
+# Install dependencies
+pip install -r requirements.txt
+
+# Run tests
+pytest
+
+# Start development server
+python manage.py runserver
+```
+
 ## Project Overview
 ...

[Full diff shown]

Apply these changes? [Y/n] y

Optimization Complete!
- Previous score: 72/100
- New score: 89/100
- Lines reduced: 245 → 198 (-19%)
- Issues resolved: 4/4

Backup saved to: .claude/backups/CLAUDE.md.2025-01-18
```

## Safety Features

### Backup Creation
- Automatic backup before changes
- Stored in `.claude/backups/`
- Easy restoration if needed

### Preview Mode
- All changes shown before applying
- Diff format for easy review
- Option to approve/reject

### Selective Application
- Can apply individual changes
- Skip specific optimizations
- Iterative refinement

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Show changes without applying |
| `--no-backup` | Skip backup creation |
| `--aggressive` | Maximum condensation |
| `--preserve-comments` | Keep all existing comments |
| `--section=NAME` | Optimize specific section only |

## When to Use

Run `/config-optimize` when:
- Analysis shows score below 70
- File has grown too long
- Structure needs reorganization
- Missing critical sections
- After major refactoring

## Best Practices

1. **Run analysis first** - Understand current state
2. **Review preview carefully** - Ensure nothing important lost
3. **Test after changes** - Verify Claude follows instructions
4. **Keep backups** - Restore if issues arise
5. **Iterate** - Multiple small optimizations beat one large one

## Rollback

If optimization causes issues:

```bash
# Restore from backup
cp .claude/backups/CLAUDE.md.TIMESTAMP ./CLAUDE.md
```

Or ask:
```
Restore CLAUDE.md from the most recent backup
```
