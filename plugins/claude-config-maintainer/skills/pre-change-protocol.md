# Pre-Change Protocol

This skill defines the mandatory Pre-Change Protocol section that MUST be included in every CLAUDE.md file.

## Why This Is Mandatory

The Pre-Change Protocol prevents the #1 cause of bugs from AI-assisted coding: **incomplete changes where Claude modifies some files but misses others that reference the same code**.

Without this protocol:
- Claude may rename a function but miss callers
- Claude may modify a config but miss documentation
- Claude may update a schema but miss dependent code

## Detection

Search CLAUDE.md for these indicators:
- Header containing "Pre-Change" or "Before Any Code Change"
- References to `grep -rn` or impact search
- Checklist with "Files That Will Be Affected"
- User verification checkpoint

## Required Section Content

```markdown
## MANDATORY: Before Any Code Change

**Claude MUST show this checklist BEFORE editing any file:**

### 1. Impact Search Results
Run and show output of:
```bash
grep -rn "PATTERN" --include="*.sh" --include="*.md" --include="*.json" --include="*.py" | grep -v ".git"
```

### 2. Files That Will Be Affected
Numbered list of every file to be modified, with the specific change for each.

### 3. Files Searched But Not Changed (and why)
Proof that related files were checked and determined unchanged.

### 4. Documentation That References This
List of docs that mention this feature/script/function.

**User verifies this list before Claude proceeds. If Claude skips this, stop immediately.**

### After Changes
Run the same grep and show results proving no references remain unaddressed.
```

## Placement

Insert Pre-Change Protocol section:
- **After:** Critical Rules section
- **Before:** Common Operations section

## If Missing During Analysis

Flag as **HIGH PRIORITY** issue:

```
1. [HIGH] Missing Pre-Change Protocol section
   CLAUDE.md lacks mandatory dependency-check protocol.
   Impact: Claude may miss file references when making changes,
   leading to broken dependencies and incomplete updates.

   Recommendation: Add Pre-Change Protocol section immediately.
   This is the #1 cause of cascading bugs from incomplete changes.
```

## If Missing During Optimization

**Automatically add the section** at the correct position. This is the highest priority enhancement.

## Variations

The exact wording can vary, but these elements are required:

1. **Search requirement** - Must run grep/search before changes
2. **Affected files list** - Must enumerate all files to modify
3. **Non-affected files proof** - Must show what was checked but unchanged
4. **Documentation check** - Must list referencing docs
5. **User checkpoint** - Must pause for user verification
6. **Post-change verification** - Must verify after changes
