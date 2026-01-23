---
description: Run diagnostics and create structured issue in marketplace repository
---

# Debug Report

Run diagnostic checks on projman MCP tools and create a structured issue in the marketplace repository for investigation.

## Prerequisites

Your project `.env` must have:

```env
PROJMAN_MARKETPLACE_REPO=personal-projects/leo-claude-mktplace
```

If not configured, ask the user for the marketplace repository path.

## CRITICAL: Execution Steps

You MUST follow these steps in order. Do NOT skip any step.

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

### Step 3: Run Diagnostic Suite

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

### Step 4: Analyze Results

Count failures and categorize errors:

| Category | Indicators |
|----------|------------|
| Parameter Format | "owner/repo format", "missing parameter" |
| Authentication | "401", "403", "unauthorized" |
| Not Found | "404", "not found" |
| Network | "connection", "timeout", "ECONNREFUSED" |
| Logic | Unexpected response format, wrong data |

For each failure, write a hypothesis about the likely cause.

### Step 5: Generate Smart Labels

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

### Step 6: Generate Issue Content

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

*Generated by /debug-report - Labels: Type: Bug, Source: Diagnostic, Agent: Claude*
```

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

The diagnostic labels to apply are:
- `Source/Diagnostic` (always)
- `Type/Bug` (always)

```bash
# Fetch all labels and extract IDs for our target labels
LABELS_JSON=$(curl -s "${GITEA_API_URL}/repos/${MARKETPLACE_REPO}/labels" \
  -H "Authorization: token ${GITEA_API_TOKEN}")

# Extract label IDs (handles both org and repo labels)
SOURCE_DIAG_ID=$(echo "$LABELS_JSON" | jq -r '.[] | select(.name == "Source/Diagnostic") | .id')
TYPE_BUG_ID=$(echo "$LABELS_JSON" | jq -r '.[] | select(.name == "Type/Bug") | .id')

# Build label array (only include IDs that were found)
LABEL_IDS="[]"
if [[ -n "$SOURCE_DIAG_ID" && -n "$TYPE_BUG_ID" ]]; then
  LABEL_IDS="[$SOURCE_DIAG_ID, $TYPE_BUG_ID]"
elif [[ -n "$SOURCE_DIAG_ID" ]]; then
  LABEL_IDS="[$SOURCE_DIAG_ID]"
elif [[ -n "$TYPE_BUG_ID" ]]; then
  LABEL_IDS="[$TYPE_BUG_ID]"
fi

echo "Label IDs to apply: $LABEL_IDS"
```

**3. Create issue with labels via curl:**

```bash
# Create temp files with restrictive permissions
DIAG_TITLE=$(mktemp -t diag-title.XXXXXX)
DIAG_BODY=$(mktemp -t diag-body.XXXXXX)
DIAG_PAYLOAD=$(mktemp -t diag-payload.XXXXXX)

# Save title
echo "[Diagnostic] [summary of main failure]" > "$DIAG_TITLE"

# Save body (paste Step 6 content) - heredoc delimiter prevents shell expansion
cat > "$DIAG_BODY" << 'DIAGNOSTIC_EOF'
[Paste the full issue content from Step 6 here]
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

Display summary:

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

## DO NOT

- **DO NOT** attempt to fix anything - only report
- **DO NOT** create issues if all tests pass (just report success)
- **DO NOT** skip any diagnostic test
- **DO NOT** call MCP tools without the `repo` parameter
- **DO NOT** ask user questions during execution - run autonomously
- **DO NOT** use MCP tools to create issues in the marketplace - always use curl (avoids branch restrictions)

## If All Tests Pass

If all 5 tests pass, report success without creating an issue:

```
Debug Report Complete
=====================

Project: [PROJECT_REPO]
Tests Run: 5
Passed: 5
Failed: 0

All diagnostics passed. No issues to report.

If you're experiencing a specific problem, please describe it
and I can create a manual bug report.
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
