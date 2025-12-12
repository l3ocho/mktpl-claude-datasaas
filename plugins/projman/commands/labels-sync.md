---
description: Synchronize label taxonomy from Gitea and update suggestion logic
---

# Sync Label Taxonomy from Gitea

This command synchronizes the label taxonomy from Gitea (organization + repository labels) and updates the local reference file used by the label suggestion logic.

## Why Label Sync Matters

The label taxonomy is **dynamic** - new labels may be added to Gitea over time:
- Organization-level labels (shared across all repos)
- Repository-specific labels (unique to this project)

**Dynamic approach:** Never hardcode labels. Always fetch from Gitea and adapt suggestions accordingly.

## What This Command Does

1. **Fetch Current Labels** - Uses `get_labels` MCP tool to fetch all labels (org + repo)
2. **Compare with Local Reference** - Checks against `skills/label-taxonomy/labels-reference.md`
3. **Detect Changes** - Identifies new, removed, or modified labels
4. **Explain Changes** - Shows what changed and why it matters
5. **Update Reference** - Updates the local labels-reference.md file
6. **Confirm Update** - Asks for user confirmation before updating

## MCP Tools Used

**Gitea Tools:**
- `get_labels` - Fetch all labels (organization + repository)

The command will parse the response and categorize labels by namespace and color.

## Expected Output

```
Label Taxonomy Sync
===================

Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 28
- Repository Labels: 16
- Total: 44 labels

Comparing with local reference...

Changes Detected:
✨ NEW: Type/Performance (org-level)
   Description: Performance optimization tasks
   Color: #FF6B6B
   Suggestion: Add to suggestion logic for performance-related work

✨ NEW: Tech/Redis (repo-level)
   Description: Redis-related technology
   Color: #DC143C
   Suggestion: Add to suggestion logic for caching and data store work

📝 MODIFIED: Priority/Critical
   Change: Color updated from #D73A4A to #FF0000
   Impact: Visual only, no logic change needed

❌ REMOVED: Component/Legacy
   Reason: Component deprecated and removed from codebase
   Impact: Remove from suggestion logic

Summary:
- 2 new labels added
- 1 label modified (color only)
- 1 label removed
- Total labels: 44 → 45

Label Suggestion Logic Updates:
- Type/Performance: Suggest for keywords "optimize", "performance", "slow", "speed"
- Tech/Redis: Suggest for keywords "cache", "redis", "session", "pubsub"
- Component/Legacy: Remove from all suggestion contexts

Update local reference file?
[Y/n]
```

## Label Taxonomy Structure

Labels are organized by namespace:

**Organization Labels (28):**
- `Agent/*` (2): Agent/Human, Agent/Claude
- `Complexity/*` (3): Simple, Medium, Complex
- `Efforts/*` (5): XS, S, M, L, XL
- `Priority/*` (4): Low, Medium, High, Critical
- `Risk/*` (3): Low, Medium, High
- `Source/*` (4): Development, Staging, Production, Customer
- `Type/*` (6): Bug, Feature, Refactor, Documentation, Test, Chore

**Repository Labels (16):**
- `Component/*` (9): Backend, Frontend, API, Database, Auth, Deploy, Testing, Docs, Infra
- `Tech/*` (7): Python, JavaScript, Docker, PostgreSQL, Redis, Vue, FastAPI

## Local Reference File

The command updates `skills/label-taxonomy/labels-reference.md` with:

```markdown
# Label Taxonomy Reference

Last synced: 2025-01-18 14:30 UTC
Source: Gitea (bandit/your-repo-name)

## Organization Labels (28)

### Agent (2)
- Agent/Human - Work performed by human developers
- Agent/Claude - Work performed by Claude Code

### Type (6)
- Type/Bug - Bug fixes and error corrections
- Type/Feature - New features and enhancements
- Type/Refactor - Code restructuring and architectural changes
- Type/Documentation - Documentation updates
- Type/Test - Testing-related work
- Type/Chore - Maintenance and tooling tasks

...

## Repository Labels (16)

### Component (9)
- Component/Backend - Backend service code
- Component/Frontend - User interface code
- Component/API - API endpoints and contracts
...

## Suggestion Logic

When suggesting labels, consider:

**Type Detection:**
- Keywords "bug", "fix", "error" → Type/Bug
- Keywords "feature", "add", "implement" → Type/Feature
- Keywords "refactor", "extract", "restructure" → Type/Refactor
...
```

## When to Run

Run `/labels-sync` when:
- Setting up the plugin for the first time
- You notice missing labels in suggestions
- New labels are added to Gitea (announced by team)
- Quarterly maintenance (check for changes)
- After major taxonomy updates

## Integration with Other Commands

The updated taxonomy is used by:
- `/sprint-plan` - Planner agent uses `suggest_labels` with current taxonomy
- All commands that create or update issues

## Example Usage

```
User: /labels-sync

Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 28
- Repository Labels: 16
- Total: 44 labels

Comparing with local reference...

✅ No changes detected. Label taxonomy is up to date.

Last synced: 2025-01-18 14:30 UTC

User: /labels-sync

Fetching labels from Gitea...

Changes Detected:
✨ NEW: Type/Performance
✨ NEW: Tech/Redis

Update local reference file? [Y/n] y

✅ Label taxonomy updated successfully!
✅ Suggestion logic updated with new labels

New labels available for use:
- Type/Performance
- Tech/Redis
```

## Troubleshooting

**Error: Cannot fetch labels from Gitea**
- Check your Gitea configuration in `~/.config/claude/gitea.env`
- Verify your API token has `read:org` and `repo` permissions
- Ensure you're connected to the network

**Error: Permission denied to update reference file**
- Check file permissions on `skills/label-taxonomy/labels-reference.md`
- Ensure you have write access to the plugin directory

**No changes detected but labels seem wrong**
- The reference file may be manually edited - review it
- Try forcing a re-sync by deleting the reference file first
- Check if you're comparing against the correct repository

## Best Practices

1. **Sync regularly** - Run monthly or when notified of label changes
2. **Review changes** - Always review what changed before confirming
3. **Update planning** - After sync, consider if new labels affect current sprint
4. **Communicate changes** - Let team know when new labels are available
5. **Keep skill updated** - The label-taxonomy skill should match the reference file
