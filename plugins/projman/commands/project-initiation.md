---
description: Discover, analyze, and charter a new project
agent: planner
---

# /project initiation

## Purpose

Analyze an existing codebase or system description, create a project charter, and decompose into epics.

## Skills Required

- skills/source-analysis.md — analysis framework
- skills/project-charter.md — charter template and naming
- skills/epic-conventions.md — epic decomposition rules
- skills/wiki-conventions.md — page naming and dependency headers
- skills/visual-output.md — output formatting

## Workflow

### Step 1: Source Analysis
If a source codebase path is provided, analyze it using `skills/source-analysis.md`:
- Identify tech stack, architecture, features, data model, quality state
- If no source provided (greenfield), skip to Step 2

### Step 2: Project Charter
Create wiki page `Project: {Name}` following `skills/project-charter.md`:
- Set status to `Initiating`
- Fill Vision, Scope (In/Out), Source Analysis Summary (if applicable)
- Leave Architecture Decisions, Epic Decomposition, Roadmap as placeholders

### Step 3: Epic Decomposition
Using analysis results, decompose project into epics per `skills/epic-conventions.md`:
- Create `Epic/*` labels if they don't exist (check with `list_labels`)
- Fill the Epic Decomposition table in the charter

### Step 4: Present and Confirm
Show the charter to the user. Wait for approval before proceeding to `/project plan`.

## Output

- Wiki page: `Project: {Name}`
- Labels: `Epic/*` labels created in Gitea
- State: `Initiating` — awaiting `/project plan`

## DO NOT

- Create sprint issues — that's `/sprint plan`
- Create WBS or roadmap — that's `/project plan`
- Make architecture decisions — suggest ADRs via `/adr create`
- Skip user approval of the charter
