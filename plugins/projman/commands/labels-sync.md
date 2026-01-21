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

1. **Auto-Detect Repository** - Automatically detects repo from git remote (or uses explicit `repo` param)
2. **Check Owner Type** - Determines if owner is organization or user account
3. **Fetch Current Labels** - Uses `get_labels` MCP tool to fetch all labels (org + repo)
4. **Display Current Taxonomy** - Shows organization and repository label counts
5. **Identify Missing Required Labels** - Checks for required labels (Type/*, Priority/*, etc.)
6. **Create Missing Labels** - Automatically creates any missing required labels
7. **Report Status** - Summarizes what was found and created

**Note:** This command executes autonomously without user prompts. It fetches labels, reports findings, and creates missing labels automatically.

## MCP Tools Used

**Gitea Tools:**
- `get_labels` - Fetch all labels (organization + repository)
- `create_label` - Create missing required labels
- `validate_repo_org` - Verify repository belongs to organization

## Required Label Categories

At minimum, these label categories must exist:

- **Type/***: Bug, Feature, Refactor, Documentation, Test, Chore
- **Priority/***: Low, Medium, High, Critical
- **Complexity/***: Simple, Medium, Complex
- **Efforts/***: XS, S, M, L, XL

If any required labels are missing, the command will offer to create them.

## Expected Output

```
Label Taxonomy Sync
===================

Auto-detecting repository from git remote...
Repository: personal-projects/your-repo-name
Owner type: Organization

Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 27
- Repository Labels: 16
- Total: 43 labels

Organization Labels by Category:
  Agent/*: 2 labels
  Complexity/*: 3 labels
  Efforts/*: 5 labels
  Priority/*: 4 labels
  Risk/*: 3 labels
  Source/*: 4 labels
  Type/*: 6 labels

Repository Labels by Category:
  Component/*: 9 labels
  Tech/*: 7 labels

Required Labels Check:
  Type/*: 6/6 present
  Priority/*: 4/4 present
  Complexity/*: 3/3 present
  Efforts/*: 5/5 present

All required labels present. Label taxonomy is ready for use.
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

## Label Reference

The plugin includes a static reference file at `skills/label-taxonomy/labels-reference.md` that documents the expected label taxonomy and suggestion logic.

**Important:** This reference file is part of the plugin package and serves as documentation. The `/labels-sync` command fetches labels dynamically from Gitea - it does not modify the reference file.

**Dynamic Approach:** Labels are always fetched fresh from Gitea using `get_labels`. The reference file provides context for the `suggest_labels` logic but is not the source of truth.

Example reference file structure:

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
- Keywords "bug", "fix", "error" -> Type/Bug
- Keywords "feature", "add", "implement" -> Type/Feature
- Keywords "refactor", "extract", "restructure" -> Type/Refactor
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

**Example 1: All labels present**
```
User: /labels-sync

Auto-detecting repository...
Repository: personal-projects/my-project
Owner type: Organization

Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 27
- Repository Labels: 16
- Total: 43 labels

Required Labels Check:
  Type/*: 6/6 present
  Priority/*: 4/4 present
  Complexity/*: 3/3 present
  Efforts/*: 5/5 present

All required labels present. Label taxonomy is ready for use.
```

**Example 2: Missing required labels (auto-created)**
```
User: /labels-sync

Auto-detecting repository...
Repository: personal-projects/new-project
Owner type: User (no organization labels available)

Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 0 (user account - no org labels)
- Repository Labels: 3
- Total: 3 labels

Required Labels Check:
  Type/*: 0/6 - MISSING: Bug, Feature, Refactor, Documentation, Test, Chore
  Priority/*: 0/4 - MISSING: Low, Medium, High, Critical
  Complexity/*: 0/3 - MISSING: Simple, Medium, Complex
  Efforts/*: 0/5 - MISSING: XS, S, M, L, XL

Creating missing required labels...
  Created: Type/Bug (#d73a4a)
  Created: Type/Feature (#0075ca)
  ... (18 total labels created)

Label taxonomy initialized. All required labels now present.
```

## Troubleshooting

**Error: Cannot fetch labels from Gitea**
- Check your Gitea configuration in `~/.config/claude/gitea.env`
- Verify your API token has `read:org` and `repo` permissions
- Ensure you're connected to the network

**Error: Use 'owner/repo' format**
- Ensure you're running from a directory with a git remote configured
- Or pass the `repo` parameter explicitly: `GITEA_REPO=owner/repo` in `.env`

**Organization labels empty for org-owned repo**
- Verify the organization has labels configured in Gitea
- Check if the owner is truly an organization (not a user account)
- User accounts don't have organization-level labels

**User-owned repo (no org labels)**
- This is expected behavior - user accounts can only have repository-level labels
- The plugin will work with repo labels only and create missing required labels

## Best Practices

1. **Sync at sprint start** - Ensure labels are current before planning
2. **Review changes** - Always review what changed before confirming
3. **Create missing required labels** - Don't skip this step
4. **Update planning** - After sync, consider if new labels affect current sprint
5. **Communicate changes** - Let team know when new labels are available
