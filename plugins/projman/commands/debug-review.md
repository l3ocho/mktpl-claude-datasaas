---
description: Investigate diagnostic issues and propose fixes with human approval
---

# Debug Review

Investigate diagnostic issues created by `/debug-report`, read relevant code, and propose fixes with human approval at each step.

## CRITICAL: This Command Requires Human Approval

This command has THREE mandatory approval gates. You MUST stop and wait for user confirmation at each gate before proceeding.

## Execution Steps

### Step 1: Detect Repository

Run Bash to get the current repository:

```bash
git remote get-url origin
```

Parse to extract `REPO_NAME` in `owner/repo` format.

### Step 2: Fetch Diagnostic Issues

```
mcp__plugin_projman_gitea__list_issues(
  repo=REPO_NAME,
  state="open",
  labels=["Source: Diagnostic"]
)
```

If no issues with that label, try without label filter and look for issues with "[Diagnostic]" in title.

### Step 3: Display Issue List

Show the user available issues:

```
Debug Review
============

Open Diagnostic Issues:

  #80 - [Diagnostic] get_labels fails without repo parameter
        Created: 2026-01-21 | Labels: Type: Bug, Source: Diagnostic

  #77 - [Diagnostic] MCP tools require explicit repo parameter
        Created: 2026-01-21 | Labels: Type: Bug, Source: Diagnostic

No diagnostic issues? Showing recent bugs:

  #75 - [Bug] Some other issue
        Created: 2026-01-20
```

### Step 4: User Selects Issue

Use AskUserQuestion:

```
Which issue would you like to investigate?
Options: [List issue numbers]
```

Wait for user selection.

### Step 5: Fetch Full Issue Details

```
mcp__plugin_projman_gitea__get_issue(repo=REPO_NAME, issue_number=SELECTED)
```

### Step 6: Parse Diagnostic Report

Extract from the issue body:

1. **Failed Tools**: Which MCP tools failed
2. **Error Messages**: Exact error text
3. **Hypothesis**: Reporter's analysis
4. **Suggested Investigation**: Files to check
5. **Project Context**: Repo, branch, cwd where error occurred

If the issue doesn't follow the diagnostic template, extract what information is available.

### Step 7: Map Errors to Code Files

Use this mapping to identify relevant files:

**By Tool Name:**
| Tool | Primary Files |
|------|---------------|
| `validate_repo_org` | `mcp-servers/gitea/mcp_server/gitea_client.py` |
| `get_labels` | `mcp-servers/gitea/mcp_server/tools/labels.py` |
| `suggest_labels` | `mcp-servers/gitea/mcp_server/tools/labels.py` |
| `list_issues` | `mcp-servers/gitea/mcp_server/tools/issues.py` |
| `create_issue` | `mcp-servers/gitea/mcp_server/tools/issues.py` |
| `list_milestones` | `mcp-servers/gitea/mcp_server/gitea_client.py` |

**By Error Pattern:**
| Error Contains | Check Files |
|----------------|-------------|
| "owner/repo format" | `config.py`, `gitea_client.py` |
| "404" + "orgs" | `gitea_client.py` (is_org_repo method) |
| "401", "403" | `config.py` (token loading) |
| "No repository" | Command `.md` file (repo detection step) |

**By Command:**
| Command | Documentation File |
|---------|-------------------|
| `/labels-sync` | `plugins/projman/commands/labels-sync.md` |
| `/sprint-plan` | `plugins/projman/commands/sprint-plan.md` |
| `/sprint-start` | `plugins/projman/commands/sprint-start.md` |
| `/debug-report` | `plugins/projman/commands/debug-report.md` |

### Step 8: Read Relevant Files (MANDATORY)

You MUST read the identified files before proposing any fix.

For each relevant file:
1. Read the file using the Read tool
2. Find the specific function/method mentioned in the error
3. Understand the code path that leads to the error
4. Note any related code that might be affected

Display snippets of relevant code to the user:

```
Reading relevant files...

┌─ mcp-servers/gitea/mcp_server/tools/labels.py (lines 29-40) ────────┐
│                                                                      │
│ async def get_labels(self, repo: Optional[str] = None):              │
│     target_repo = repo or self.gitea.repo                            │
│     if not target_repo or '/' not in target_repo:                    │
│         raise ValueError("Use 'owner/repo' format...")               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Step 9: Present Investigation Summary

Summarize what you found:

```
Investigation Summary
=====================

ISSUE: #80 - get_labels fails without repo parameter

FAILED TOOLS:
  • get_labels - "Use 'owner/repo' format"

CODE ANALYSIS:

1. labels.py:get_labels() requires repo parameter
   - Line 30: `target_repo = repo or self.gitea.repo`
   - Line 31-32: Raises ValueError if no repo

2. labels-sync.md documents Step 1 for repo detection
   - Lines 13-26: Instructs to run `git remote get-url origin`
   - This step may not be followed by executing Claude

ROOT CAUSE HYPOTHESIS:

The command documentation (labels-sync.md) correctly instructs
repo detection, but the executing Claude may be skipping Step 1
and calling MCP tools directly.

Evidence:
  • Error indicates repo parameter was not passed
  • labels-sync.md has correct instructions
  • MCP server cannot auto-detect (sandboxed environment)

LIKELY FIX:

Option A: Make Step 1 more prominent in labels-sync.md
Option B: Add validation that repo was detected before proceeding
Option C: [Other based on analysis]
```

## APPROVAL GATE 1

```
Does this analysis match your understanding of the problem?

[Y] Yes, proceed to propose fix
[N] No, let me clarify
[R] Read more files first
```

**STOP HERE AND WAIT FOR USER RESPONSE**

Do NOT proceed until user approves.

### Step 9.5: Search Lessons Learned

Before proposing a fix, search for relevant lessons from past fixes.

**1. Extract search tags from the issue:**

```
SEARCH_TAGS = []
# Add tool names
for each failed_tool in issue:
  SEARCH_TAGS.append(tool_name)  # e.g., "get_labels", "validate_repo_org"

# Add error category
SEARCH_TAGS.append(error_category)  # e.g., "parameter-format", "authentication"

# Add component if identifiable
if error relates to MCP server:
  SEARCH_TAGS.append("mcp")
if error relates to command:
  SEARCH_TAGS.append("command")
```

**2. Search lessons learned:**

```
mcp__plugin_projman_gitea__search_lessons(
  repo=REPO_NAME,
  tags=SEARCH_TAGS,
  limit=5
)
```

**3. Also search by error keywords:**

```
mcp__plugin_projman_gitea__search_lessons(
  repo=REPO_NAME,
  query=[key error message words],
  limit=5
)
```

**4. Display relevant lessons (if any):**

```
Related Lessons Learned
=======================

Found [N] relevant lessons from past fixes:

📚 Lesson: "Sprint 14 - Parameter validation in MCP tools"
   Tags: mcp, get_labels, parameter-format
   Summary: Always validate repo parameter format before API calls
   Prevention: Add format check at function entry

📚 Lesson: "Sprint 12 - Graceful fallback for missing config"
   Tags: configuration, fallback
   Summary: Commands should work even without .env
   Prevention: Check for env vars, use sensible defaults

These lessons may inform your fix approach.
```

If no lessons found, display:
```
No related lessons found. This may be a new type of issue.
```

### Step 10: Propose Fix Approach

Based on the analysis, propose a specific fix:

```
Proposed Fix
============

APPROACH: [A/B/C from above]

CHANGES NEEDED:

1. File: plugins/projman/commands/labels-sync.md
   Change: Add warning box after Step 1 emphasizing repo must be detected

2. File: [if applicable]
   Change: [description]

RATIONALE:

[Explain why this fix addresses the root cause]

RISKS:

[Any potential issues with this approach]
```

## APPROVAL GATE 2

```
Proceed with this fix approach?

[Y] Yes, implement it
[N] No, try different approach
[M] Modify the approach (tell me what to change)
```

**STOP HERE AND WAIT FOR USER RESPONSE**

Do NOT implement until user approves.

### Step 11: Implement Fix

Only after user approves:

1. Create feature branch:
```bash
git checkout -b fix/issue-[NUMBER]-[brief-description]
```

2. Make the code changes using Edit tool

3. Run relevant tests if they exist:
```bash
cd mcp-servers/gitea && .venv/bin/python -m pytest tests/ -v
```

4. Show the changes to user:
```bash
git diff
```

### Step 12: Present Changes

```
Changes Implemented
===================

Branch: fix/issue-80-labels-sync-instructions

Files Modified:
  • plugins/projman/commands/labels-sync.md (+15, -3)

Diff Summary:
[Show git diff output]

Test Results:
  • 23 passed, 0 failed (or N/A if no tests)
```

## APPROVAL GATE 3

```
Create PR with these changes?

[Y] Yes, create PR
[N] No, I want to modify something
[D] Discard changes
```

**STOP HERE AND WAIT FOR USER RESPONSE**

Do NOT create PR until user approves.

### Step 13: Create PR

Only after user approves:

1. Commit changes:
```bash
git add -A
git commit -m "fix: [description]

[Longer explanation]

Fixes #[ISSUE_NUMBER]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

2. Push branch:
```bash
git push -u origin fix/issue-[NUMBER]-[brief-description]
```

3. Create PR via API or MCP tools

4. **Switch back to development branch** (required for MCP issue operations):
```bash
git checkout development
```

5. Add comment to original issue:
```
mcp__plugin_projman_gitea__add_comment(
  repo=REPO_NAME,
  issue_number=ISSUE_NUMBER,
  comment="Fix proposed in PR #[PR_NUMBER]\n\nChanges:\n- [summary]\n\nPlease test after merge and report back."
)
```

### Step 14: Report Completion

```
Debug Review Complete
=====================

Issue: #80 - get_labels fails without repo parameter
Status: Fix Proposed

PR Created: #81 - fix: improve labels-sync repo detection instructions
URL: http://gitea.hotserv.cloud/.../pulls/81

Next Steps:
  1. Review and merge PR #81
  2. In test project, pull latest plugin version
  3. Run /debug-report to verify fix
  4. Come back and run Step 15 to close issue and capture lesson
```

### Step 15: Verify, Close, and Capture Lesson

**This step runs AFTER the user has verified the fix works.**

When user returns and confirms the fix is working:

**1. Close the issue:**

```
mcp__plugin_projman_gitea__update_issue(
  repo=REPO_NAME,
  issue_number=ISSUE_NUMBER,
  state="closed"
)
```

**2. Ask about lesson capture:**

Use AskUserQuestion:

```
This fix addressed [ERROR_TYPE] in [COMPONENT].

Would you like to capture this as a lesson learned?

Options:
- Yes, capture lesson (helps avoid similar issues in future)
- No, skip (trivial fix or already documented)
```

**3. If user chooses Yes, auto-generate lesson content:**

```
LESSON_TITLE = "Sprint [N] - [Brief description of fix]"
  # Example: "Sprint 17 - MCP parameter validation"

LESSON_CONTENT = """
## Context

[What was happening when the issue occurred]
- Command/tool being used: [FAILED_TOOL]
- Error encountered: [ERROR_MESSAGE]

## Problem

[Root cause identified during investigation]

## Solution

[What was changed to fix it]
- Files modified: [LIST]
- PR: #[PR_NUMBER]

## Prevention

[How to avoid this in the future]

## Related

- Issue: #[ISSUE_NUMBER]
- PR: #[PR_NUMBER]
"""

LESSON_TAGS = [
  tool_name,        # e.g., "get_labels"
  error_category,   # e.g., "parameter-format"
  component,        # e.g., "mcp", "command"
  "bug-fix"
]
```

**4. Show lesson preview and ask for approval:**

```
Lesson Preview
==============

Title: [LESSON_TITLE]
Tags: [LESSON_TAGS]

Content:
[LESSON_CONTENT]

Save this lesson? (Y/N/Edit)
```

**5. If approved, create the lesson:**

```
mcp__plugin_projman_gitea__create_lesson(
  repo=REPO_NAME,
  title=LESSON_TITLE,
  content=LESSON_CONTENT,
  tags=LESSON_TAGS,
  category="sprints"
)
```

**6. Report completion:**

```
Issue Closed & Lesson Captured
==============================

Issue #[N]: CLOSED
Lesson: "[LESSON_TITLE]" saved to wiki

This lesson will be surfaced in future /debug-review
sessions when similar errors are encountered.
```

## DO NOT

- **DO NOT** skip reading relevant files - this is MANDATORY
- **DO NOT** proceed past approval gates without user confirmation
- **DO NOT** guess at fixes without evidence from code
- **DO NOT** close issues until user confirms fix works (Step 15)
- **DO NOT** commit directly to development or main branches
- **DO NOT** skip the lessons learned search - past fixes inform better solutions

## If Investigation Finds No Bug

Sometimes investigation reveals the issue is:
- User error (didn't follow documented steps)
- Configuration issue (missing .env vars)
- Already fixed in a newer version

In this case:

```
Investigation Summary
=====================

FINDING: This does not appear to be a code bug.

ANALYSIS:
[Explanation of what you found]

RECOMMENDATION:
[ ] Close issue as "not a bug" - user error
[ ] Close issue as "duplicate" of #[X]
[ ] Add documentation to prevent confusion
[ ] Other: [specify]

Would you like me to add a comment explaining this finding?
```

## Error-to-File Quick Reference

```
Error Message                    → File to Check
─────────────────────────────────────────────────────────────────
"Use 'owner/repo' format"        → config.py, gitea_client.py
"404 Client Error.*orgs"         → gitea_client.py (_is_organization)
"No repository specified"        → Command .md file (Step 1)
"401 Unauthorized"               → config.py (token loading)
"labels not found"               → labels.py, gitea_client.py
"create local.*file"             → Command .md file (DO NOT section)
```
