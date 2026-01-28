# /pr-summary - Quick PR Summary

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 PR-REVIEW · Quick Summary                                     │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the summary.

## Purpose

Generate a quick summary of PR changes without conducting a full multi-agent review.

## Usage

```
/pr-summary <pr-number> [--repo owner/repo]
```

## Behavior

### Step 1: Fetch PR Data

Using Gitea MCP tools:
1. `get_pull_request` - PR metadata
2. `get_pr_diff` - Code changes

### Step 2: Analyze Changes

Quick analysis of:
- Files modified
- Types of changes (features, fixes, refactoring)
- Scope and impact

### Step 3: Generate Summary

```
═══════════════════════════════════════════════════
PR Summary: #123 - Add user authentication
═══════════════════════════════════════════════════

Author: @johndoe
Branch: feat/user-auth → development
Status: Open (ready for review)

───────────────────────────────────────────────────
CHANGES OVERVIEW
───────────────────────────────────────────────────

Files: 12 changed
  + 8 new files
  ~ 3 modified files
  - 1 deleted file

Lines: +234 / -45 (net +189)

───────────────────────────────────────────────────
WHAT THIS PR DOES
───────────────────────────────────────────────────

This PR adds user authentication functionality:

1. **New API endpoints**
   - POST /api/auth/login
   - POST /api/auth/register
   - POST /api/auth/logout

2. **Frontend components**
   - LoginForm component
   - RegisterForm component
   - Auth context provider

3. **Database changes**
   - New users table
   - Sessions table

───────────────────────────────────────────────────
KEY FILES
───────────────────────────────────────────────────

• src/api/auth/login.ts (+85) - Login endpoint
• src/api/auth/register.ts (+120) - Registration
• src/components/LoginForm.tsx (+65) - Login UI
• src/db/migrations/001_users.sql (+45) - Schema

───────────────────────────────────────────────────
QUICK ASSESSMENT
───────────────────────────────────────────────────

Scope: Medium (authentication feature)
Risk: Medium (new security-sensitive code)
Recommendation: Full /pr-review suggested

═══════════════════════════════════════════════════
```

## Output

Summary report with:
- PR metadata
- Change statistics
- Plain-language description of changes
- Key files list
- Quick risk assessment

## When to Use

- Get quick overview before full review
- Triage multiple PRs
- Understand PR scope
