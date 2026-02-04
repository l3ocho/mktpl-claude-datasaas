---
description: Diagnose issues and create reports, or investigate existing diagnostic issues
---

# PM Debug

## Skills Required

- skills/mcp-tools-reference.md
- skills/lessons-learned.md
- skills/git-workflow.md

## Purpose

Unified debugging command for diagnostics and issue investigation.

## Invocation

```
/pm-debug              # Ask which mode
/pm-debug report       # Run diagnostics, create issue
/pm-debug review       # Investigate existing issues
```

## Mode Selection

If no subcommand provided, ask user:

1. **Report** - Run MCP tool diagnostics and create issue in marketplace
2. **Review** - Investigate existing diagnostic issues and propose fixes

---

## Mode: Report

Create structured issues in the marketplace repository.

### Prerequisites

Project `.env` must have:
```env
PROJMAN_MARKETPLACE_REPO=personal-projects/leo-claude-mktplace
```

### Workflow

#### Step 0: Select Report Type
- **Automated** - Run MCP tool diagnostics and report failures
- **User-Reported** - Gather structured feedback about a problem

#### For User-Reported (Step 0.1)
Gather via AskUserQuestion:
1. Which plugin/command was affected
2. What was the goal
3. What type of problem (error, missing feature, unexpected behavior, docs)
4. Problem description
5. Expected behavior
6. Workaround (optional)

#### Steps 1-2: Context Gathering
1. Gather project context (git remote, branch, pwd)
2. Detect sprint context (active milestone)
3. Read marketplace config

#### Steps 3-4: Diagnostic Suite (Automated Only)
Run MCP tools with explicit `repo` parameter:
- `validate_repo_org`
- `get_labels`
- `list_issues`
- `list_milestones`
- `suggest_labels`

Categorize: Parameter Format, Authentication, Not Found, Network, Logic

#### Steps 5-6: Generate Labels and Issue
**Automated:** `Type/Bug`, `Source/Diagnostic`, `Agent/Claude` + suggested
**User-Reported:** Map problem type to labels

#### Step 7: Create Issue
**Use curl (not MCP)** - avoids branch protection issues

#### Step 8: Report to User
Show summary and link to created issue

### DO NOT (Report Mode)
- Attempt to fix anything - only report
- Create issues if all automated tests pass (unless user-reported)
- Use MCP tools to create issues in marketplace - always use curl

---

## Mode: Review

Investigate diagnostic issues and propose fixes with human approval.

### Workflow with Approval Gates

#### Steps 1-8: Investigation
1. Detect repository (git remote)
2. Fetch diagnostic issues: `list_issues(labels=["Source: Diagnostic"])`
3. Display issue list
4. User selects issue (AskUserQuestion)
5. Fetch full details: `get_issue(issue_number=...)`
6. Parse diagnostic report (failed tools, errors, hypothesis)
7. Map errors to files
8. Read relevant files - **MANDATORY before proposing fix**

#### Step 9: Investigation Summary
Present analysis to user.

**APPROVAL GATE 1:** "Does this analysis match your understanding?"
- STOP and wait for user response

#### Step 9.5: Search Lessons Learned
Search for related past fixes using `search_lessons`.

#### Step 10: Propose Fix
Present specific fix approach with changes and rationale.

**APPROVAL GATE 2:** "Proceed with this fix?"
- STOP and wait for user response

#### Steps 11-12: Implement
1. Create feature branch (`fix/issue-N-description`)
2. Make code changes
3. Run tests
4. Show diff to user

**APPROVAL GATE 3:** "Create PR with these changes?"
- STOP and wait for user response

#### Steps 13-15: Finalize
13. Commit and push
14. Create PR
15. After user verifies fix: Close issue (REQUIRED) and capture lesson

### Error-to-File Quick Reference

| Error Pattern | Check Files |
|---------------|-------------|
| "owner/repo format" | config.py, gitea_client.py |
| "404" + "orgs" | gitea_client.py |
| "401", "403" | config.py (token) |
| "No repository" | Command .md file |

### DO NOT (Review Mode)
- Skip reading relevant files
- Proceed past approval gates without confirmation
- Close issues until user confirms fix works
- Commit directly to development/main

---

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🔧 DEBUG                                                        ║
║  [Mode: Report | Review]                                         ║
╚══════════════════════════════════════════════════════════════════╝
```
