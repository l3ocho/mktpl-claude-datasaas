---
description: Run diagnostics and create structured issue in marketplace repository
---

# Debug Report

Create structured issues in the marketplace repository - either from automated diagnostic tests OR from user-reported problems.

## Prerequisites

Your project `.env` must have:

```env
PROJMAN_MARKETPLACE_REPO=personal-projects/leo-claude-mktplace
```

If not configured, ask the user for the marketplace repository path.

## CRITICAL: Execution Steps

You MUST follow these steps in order. Do NOT skip any step.

### Step 0: Select Report Mode

Use AskUserQuestion to determine what the user wants to report:

```
What would you like to report?

[ ] Run automated diagnostics - Test MCP tools and report failures
[ ] Report an issue I experienced - Describe a problem with any plugin command
```

Store the selection as `REPORT_MODE`:
- "automated" → Continue to Step 1
- "user-reported" → Skip to Step 0.1

---

### Step 0.1: Gather User Feedback (User-Reported Mode Only)

If `REPORT_MODE` is "user-reported", gather structured feedback.

**Question 1: What were you trying to do?**

Use AskUserQuestion:
```
Which plugin/command were you using?

[ ] projman (sprint planning, issues, labels)
[ ] git-flow (commits, branches)
[ ] pr-review (pull request review)
[ ] cmdb-assistant (NetBox integration)
[ ] doc-guardian (documentation)
[ ] code-sentinel (security, refactoring)
[ ] Other - I'll describe it
```

Store as `AFFECTED_PLUGIN`.

Then ask for the specific command (free text):
```
What command or tool were you using? (e.g., /sprint-plan, virt_update_vm)
```

Store as `AFFECTED_COMMAND`.

**Question 2: What was your goal?**

```
Briefly describe what you were trying to accomplish:
```

Store as `USER_GOAL`.

**Question 3: What went wrong?**

Use AskUserQuestion:
```
What type of problem did you encounter?

[ ] Error message - Command failed with an error
[ ] Missing feature - Tool doesn't support what I need
[ ] Unexpected behavior - It worked but did the wrong thing
[ ] Documentation issue - Instructions were unclear or wrong
[ ] Other - I'll describe it
```

Store as `PROBLEM_TYPE`.

Then ask for details (free text):
```
Describe what happened. Include any error messages if applicable:
```

Store as `PROBLEM_DESCRIPTION`.

**Question 4: Expected vs Actual**

```
What did you expect to happen?
```

Store as `EXPECTED_BEHAVIOR`.

**Question 5: Workaround (optional)**

```
Did you find a workaround? If so, describe it (or skip):
```

Store as `WORKAROUND` (may be empty).

After gathering feedback, continue to Step 1 for context gathering, then skip to Step 5.1.

---

### Step 1: Gather Project Context

Run these Bash commands to capture project information:

```bash
# Get git remote URL
git remote get-url origin

# Get current branch
git branch --show-current

# Get working directory
pwd
```

Parse the git remote to extract `REPO_NAME` in `owner/repo` format.

Store all values:
- `PROJECT_REPO`: The detected owner/repo
- `GIT_REMOTE`: Full git remote URL
- `CURRENT_BRANCH`: Current branch name
- `WORKING_DIR`: Current working directory

### Step 1.5: Detect Sprint Context

Determine if this debug issue should be associated with an active sprint.

**1. Check for active sprint milestone:**

```
mcp__plugin_projman_gitea__list_milestones(repo=PROJECT_REPO, state="open")
```

Store the first open milestone as `ACTIVE_SPRINT` (if any).

**2. Analyze branch context:**

| Branch Pattern | Context |
|----------------|---------|
| `feat/*`, `fix/*`, `issue-*` | Sprint work - likely related to current sprint |
| `main`, `master`, `development` | Production/standalone - not sprint-related |
| Other | Unknown - ask user |

**3. Determine sprint association:**

```
IF ACTIVE_SPRINT exists AND CURRENT_BRANCH matches sprint pattern (feat/*, fix/*, issue-*):
  → SPRINT_CONTEXT = "detected"
  → Ask user: "Active sprint detected: [SPRINT_NAME]. Is this bug related to sprint work?"
    Options:
    - Yes, add to sprint (will associate with milestone)
    - No, standalone fix (no milestone)
  → Store choice as ASSOCIATE_WITH_SPRINT (true/false)

ELSE IF ACTIVE_SPRINT exists AND CURRENT_BRANCH is main/development:
  → SPRINT_CONTEXT = "production"
  → ASSOCIATE_WITH_SPRINT = false (standalone fix, no question needed)

ELSE:
  → SPRINT_CONTEXT = "none"
  → ASSOCIATE_WITH_SPRINT = false
```

### Step 2: Read Marketplace Configuration

```bash
grep PROJMAN_MARKETPLACE_REPO .env
```

Store as `MARKETPLACE_REPO`. If not found, ask the user.

### Step 3: Run Diagnostic Suite (Automated Mode Only)

**Skip this step if `REPORT_MODE` is "user-reported"** → Go to Step 5.1

Run each MCP tool with explicit `repo` parameter. Record success/failure and full response.

**Test 1: validate_repo_org**
```
mcp__plugin_projman_gitea__validate_repo_org(repo=PROJECT_REPO)
```
Expected: `{is_organization: true/false}`

**Test 2: get_labels**
```
mcp__plugin_projman_gitea__get_labels(repo=PROJECT_REPO)
```
Expected: `{organization: [...], repository: [...], total_count: N}`

**Test 3: list_issues**
```
mcp__plugin_projman_gitea__list_issues(repo=PROJECT_REPO, state="open")
```
Expected: Array of issues

**Test 4: list_milestones**
```
mcp__plugin_projman_gitea__list_milestones(repo=PROJECT_REPO)
```
Expected: Array of milestones

**Test 5: suggest_labels**
```
mcp__plugin_projman_gitea__suggest_labels(context="Test bug fix for authentication")
```
Expected: Array of label names matching repo's format

For each test, record:
- Tool name
- Exact parameters used
- Status: PASS or FAIL
- Response or error message

### Step 4: Analyze Results (Automated Mode Only)

**Skip this step if `REPORT_MODE` is "user-reported"** → Go to Step 5.1

Count failures and categorize errors:

| Category | Indicators |
|----------|------------|
| Parameter Format | "owner/repo format", "missing parameter" |
| Authentication | "401", "403", "unauthorized" |
| Not Found | "404", "not found" |
| Network | "connection", "timeout", "ECONNREFUSED" |
| Logic | Unexpected response format, wrong data |

For each failure, write a hypothesis about the likely cause.

### Step 5: Generate Smart Labels (Automated Mode Only)

**Skip this step if `REPORT_MODE` is "user-reported"** → Go to Step 5.1

Generate appropriate labels based on the diagnostic results.

**1. Build context string for label suggestion:**

```
LABEL_CONTEXT = "Bug fix: " + [summary of main failure] + ". " +
                "Failed tools: " + [list of failed tool names] + ". " +
                "Error category: " + [detected error category from Step 4]
```

**2. Get suggested labels:**

```
mcp__plugin_projman_gitea__suggest_labels(
  repo=PROJECT_REPO,
  context=LABEL_CONTEXT
)
```

**3. Merge with base labels:**

```
BASE_LABELS = ["Type: Bug", "Source: Diagnostic", "Agent: Claude"]
SUGGESTED_LABELS = [result from suggest_labels]

# Combine, avoiding duplicates
FINAL_LABELS = BASE_LABELS + [label for label in SUGGESTED_LABELS if label not in BASE_LABELS]
```

The final label set should include:
- **Always**: `Type: Bug`, `Source: Diagnostic`, `Agent: Claude`
- **If detected**: `Component: *`, `Complexity: *`, `Risk: *`, `Priority: *`

After generating labels, continue to Step 6.

---

### Step 5.1: Generate Labels (User-Reported Mode Only)

**Only execute this step if `REPORT_MODE` is "user-reported"**

**1. Map problem type to labels:**

| PROBLEM_TYPE | Labels |
|--------------|--------|
| Error message | `Type: Bug` |
| Missing feature | `Type: Enhancement` |
| Unexpected behavior | `Type: Bug` |
| Documentation issue | `Type: Documentation` |
| Other | `Type: Bug` (default) |

**2. Map plugin to component:**

| AFFECTED_PLUGIN | Component Label |
|-----------------|-----------------|
| projman | `Component: Commands` |
| git-flow | `Component: Commands` |
| pr-review | `Component: Commands` |
| cmdb-assistant | `Component: API` |
| doc-guardian | `Component: Commands` |
| code-sentinel | `Component: Commands` |
| Other | *(no component label)* |

**3. Build final labels:**

```
BASE_LABELS = ["Source: User-Reported", "Agent: Claude"]
TYPE_LABEL = [mapped from PROBLEM_TYPE]
COMPONENT_LABEL = [mapped from AFFECTED_PLUGIN, if any]

FINAL_LABELS = BASE_LABELS + TYPE_LABEL + COMPONENT_LABEL
```

After generating labels, continue to Step 6.1.

---

### Step 6: Generate Issue Content (Automated Mode Only)

**Skip this step if `REPORT_MODE` is "user-reported"** → Go to Step 6.1

Use this exact template:

```markdown
## Diagnostic Report

**Generated**: [ISO timestamp]
**Command Tested**: [What the user was trying to run, or "general diagnostic"]
**Reporter**: Claude Code via /debug-report

## Project Context

| Field | Value |
|-------|-------|
| Repository | `[PROJECT_REPO]` |
| Git Remote | `[GIT_REMOTE]` |
| Working Directory | `[WORKING_DIR]` |
| Current Branch | `[CURRENT_BRANCH]` |

## Diagnostic Results

### Test 1: validate_repo_org

**Call**: `validate_repo_org(repo="[PROJECT_REPO]")`
**Status**: [PASS/FAIL]
**Response**:
```json
[full response or error]
```

### Test 2: get_labels

**Call**: `get_labels(repo="[PROJECT_REPO]")`
**Status**: [PASS/FAIL]
**Response**:
```json
[full response or error - truncate if very long]
```

[... repeat for each test ...]

## Summary

- **Total Tests**: 5
- **Passed**: [N]
- **Failed**: [N]

### Failed Tools

[List each failed tool with its error]

### Error Category

[Check applicable categories]

### Hypothesis

[Your analysis of what's wrong and why]

### Suggested Investigation

1. [First file/function to check]
2. [Second file/function to check]
3. [etc.]

## Reproduction Steps

1. Navigate to `[WORKING_DIR]`
2. Run `[command that was being tested]`
3. Observe error at step [X]

---

*Generated by /debug-report (automated) - Labels: Type: Bug, Source: Diagnostic, Agent: Claude*
```

After generating content, continue to Step 7.

---

### Step 6.1: Generate Issue Content (User-Reported Mode Only)

**Only execute this step if `REPORT_MODE` is "user-reported"**

Use this template for user-reported issues:

```markdown
## User-Reported Issue

**Reported**: [ISO timestamp]
**Reporter**: Claude Code via /debug-report (user feedback)

## Context

| Field | Value |
|-------|-------|
| Plugin | `[AFFECTED_PLUGIN]` |
| Command/Tool | `[AFFECTED_COMMAND]` |
| Repository | `[PROJECT_REPO]` |
| Working Directory | `[WORKING_DIR]` |
| Branch | `[CURRENT_BRANCH]` |

## Problem Description

### Goal
[USER_GOAL]

### What Happened
**Problem Type**: [PROBLEM_TYPE]

[PROBLEM_DESCRIPTION]

### Expected Behavior
[EXPECTED_BEHAVIOR]

## Workaround
[WORKAROUND if provided, otherwise "None identified"]

## Investigation Hints

Based on the affected plugin/command, relevant files to check:

[Generate based on AFFECTED_PLUGIN:]

**projman:**
- `plugins/projman/commands/[AFFECTED_COMMAND].md`
- `mcp-servers/gitea/mcp_server/tools/*.py`

**git-flow:**
- `plugins/git-flow/commands/[AFFECTED_COMMAND].md`

**pr-review:**
- `plugins/pr-review/commands/[AFFECTED_COMMAND].md`
- `mcp-servers/gitea/mcp_server/tools/pull_requests.py`

**cmdb-assistant:**
- `plugins/cmdb-assistant/commands/[AFFECTED_COMMAND].md`
- `mcp-servers/netbox/mcp_server/tools/*.py`
- `mcp-servers/netbox/mcp_server/server.py` (tool schemas)

**doc-guardian / code-sentinel:**
- `plugins/[plugin]/commands/[AFFECTED_COMMAND].md`
- `plugins/[plugin]/hooks/*.md`

---

*Generated by /debug-report (user feedback) - Labels: [FINAL_LABELS]*
```

After generating content, continue to Step 7.

---

### Step 7: Create Issue in Marketplace

**IMPORTANT:** Always use curl to create issues in the marketplace repo. This avoids branch protection restrictions and MCP context issues that can block issue creation when working on protected branches.

**1. Load Gitea credentials:**

```bash
if [[ -f ~/.config/claude/gitea.env ]]; then
  source ~/.config/claude/gitea.env
  echo "Credentials loaded. API URL: $GITEA_API_URL"
else
  echo "ERROR: No credentials at ~/.config/claude/gitea.env"
fi
```

**2. Fetch label IDs from marketplace repo:**

Labels depend on `REPORT_MODE`:

**Automated mode:**
- `Source/Diagnostic` (always)
- `Type/Bug` (always)

**User-reported mode:**
- `Source/User-Reported` (always)
- Type label from Step 5.1 (Bug, Enhancement, or Documentation)
- Component label from Step 5.1 (if applicable)

```bash
# Fetch all labels from marketplace repo
LABELS_JSON=$(curl -s "${GITEA_API_URL}/repos/${MARKETPLACE_REPO}/labels" \
  -H "Authorization: token ${GITEA_API_TOKEN}")

# Extract label IDs based on FINAL_LABELS from Step 5 or 5.1
# Build LABEL_IDS array with IDs of labels that exist in the repo
# Example for automated mode:
SOURCE_ID=$(echo "$LABELS_JSON" | jq -r '.[] | select(.name == "Source/Diagnostic") | .id')
TYPE_ID=$(echo "$LABELS_JSON" | jq -r '.[] | select(.name == "Type/Bug") | .id')

# Example for user-reported mode (adjust based on FINAL_LABELS):
# SOURCE_ID=$(echo "$LABELS_JSON" | jq -r '.[] | select(.name == "Source/User-Reported") | .id')
# TYPE_ID=$(echo "$LABELS_JSON" | jq -r '.[] | select(.name == "[TYPE_LABEL]") | .id')

# Build label array from found IDs
LABEL_IDS="[$(echo "$SOURCE_ID,$TYPE_ID" | sed 's/,,*/,/g; s/^,//; s/,$//')]"
echo "Label IDs to apply: $LABEL_IDS"
```

**3. Create issue with labels via curl:**

**Title format depends on `REPORT_MODE`:**
- Automated: `[Diagnostic] [summary of main failure]`
- User-reported: `[AFFECTED_PLUGIN] [brief summary of PROBLEM_DESCRIPTION]`

```bash
# Create temp files with restrictive permissions
DIAG_TITLE=$(mktemp -t diag-title.XXXXXX)
DIAG_BODY=$(mktemp -t diag-body.XXXXXX)
DIAG_PAYLOAD=$(mktemp -t diag-payload.XXXXXX)

# Save title (format depends on REPORT_MODE)
# Automated: "[Diagnostic] [summary of main failure]"
# User-reported: "[AFFECTED_PLUGIN] [brief summary]"
echo "[Title based on REPORT_MODE]" > "$DIAG_TITLE"

# Save body (paste Step 6 or 6.1 content) - heredoc delimiter prevents shell expansion
cat > "$DIAG_BODY" << 'DIAGNOSTIC_EOF'
[Paste the full issue content from Step 6 or 6.1 here]
DIAGNOSTIC_EOF

# Build JSON payload with labels using jq
jq -n \
  --rawfile title "$DIAG_TITLE" \
  --rawfile body "$DIAG_BODY" \
  --argjson labels "$LABEL_IDS" \
  '{title: ($title | rtrimstr("\n")), body: $body, labels: $labels}' > "$DIAG_PAYLOAD"

# Create issue using the JSON file
RESULT=$(curl -s -X POST "${GITEA_API_URL}/repos/${MARKETPLACE_REPO}/issues" \
  -H "Authorization: token ${GITEA_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @"$DIAG_PAYLOAD")

# Extract and display the issue URL
echo "$RESULT" | jq -r '.html_url // "Error: " + (.message // "Unknown error")'

# Secure cleanup
rm -f "$DIAG_TITLE" "$DIAG_BODY" "$DIAG_PAYLOAD"
```

**4. If no credentials found, save report locally:**

```bash
REPORT_FILE=$(mktemp -t diagnostic-report-XXXXXX.md)
cat > "$REPORT_FILE" << 'DIAGNOSTIC_EOF'
[Paste the full issue content from Step 6 here]
DIAGNOSTIC_EOF
echo "Report saved to: $REPORT_FILE"
```

Then inform the user:

```
No Gitea credentials found at ~/.config/claude/gitea.env.

Diagnostic report saved to: [REPORT_FILE]

To create the issue manually:
1. Configure credentials: See docs/CONFIGURATION.md
2. Or create issue directly at: http://gitea.hotserv.cloud/[MARKETPLACE_REPO]/issues/new
```

### Step 8: Report to User

Display summary based on `REPORT_MODE`:

**Automated Mode:**
```
Debug Report Complete
=====================

Project: [PROJECT_REPO]
Tests Run: 5
Passed: [N]
Failed: [N]

Failed Tools:
  - [tool1]: [brief error]
  - [tool2]: [brief error]

Issue Created: [issue URL]

Next Steps:
  1. Switch to marketplace repo: cd [marketplace path]
  2. Run: /debug-review
  3. Select issue #[N] to investigate
```

**User-Reported Mode:**
```
Issue Report Complete
=====================

Plugin: [AFFECTED_PLUGIN]
Command: [AFFECTED_COMMAND]
Problem: [PROBLEM_TYPE]

Issue Created: [issue URL]

Your feedback has been captured. The development team will
investigate and may follow up with questions.

Next Steps:
  1. Switch to marketplace repo: cd [marketplace path]
  2. Run: /debug-review
  3. Select issue #[N] to investigate
```

## DO NOT

- **DO NOT** attempt to fix anything - only report
- **DO NOT** create issues if all automated tests pass (unless in user-reported mode)
- **DO NOT** skip any diagnostic test in automated mode
- **DO NOT** call MCP tools without the `repo` parameter
- **DO NOT** skip user questions in user-reported mode - gather complete feedback
- **DO NOT** use MCP tools to create issues in the marketplace - always use curl (avoids branch restrictions)

## If All Tests Pass (Automated Mode Only)

If all 5 tests pass in automated mode, report success without creating an issue:

```
Debug Report Complete
=====================

Project: [PROJECT_REPO]
Tests Run: 5
Passed: 5
Failed: 0

All diagnostics passed. No issues to report.

If you're experiencing a specific problem, run /debug-report again
and select "Report an issue I experienced" to describe it.
```

## Troubleshooting

**PROJMAN_MARKETPLACE_REPO not configured**
- Ask user: "What is the marketplace repository? (e.g., personal-projects/leo-claude-mktplace)"
- Store for this session and remind user to add to .env

**Cannot detect project repository**
- Check if in a git repository: `git rev-parse --git-dir`
- If not a git repo, ask user for the repository path

**Gitea credentials not found**
- Credentials must be at `~/.config/claude/gitea.env`
- If missing, the report will be saved locally for manual submission
- See docs/CONFIGURATION.md for setup instructions

**Labels not applied to issue**
- Verify labels exist in the marketplace repo: `Source/Diagnostic`, `Type/Bug`
- Check the label fetch output in Step 7.2 for errors
- If labels don't exist, create them first with `/labels-sync` in the marketplace repo
