---
description: Create WBS, risk register, and sprint roadmap for an initiated project
agent: planner
---

# /project plan

## Purpose

Take an approved project charter and create the planning artifacts: WBS, risk register, and sprint roadmap.

## Prerequisites

- Project charter exists (`Project: {Name}` wiki page with status `Initiating` or `Planning`)
- Epic decomposition complete in charter

## Skills Required

- skills/wbs.md — work breakdown structure
- skills/risk-register.md — risk identification and scoring
- skills/sprint-roadmap.md — sprint sequencing
- skills/project-charter.md — to update charter status
- skills/wiki-conventions.md — page naming and dependency headers
- skills/visual-output.md — output formatting

## Workflow

### Step 1: Load Charter
Read `Project: {Name}` wiki page. Verify epic decomposition is present.

### Step 2: Create WBS
Create wiki page `WBS: {Name}` per `skills/wbs.md`.

### Step 3: Create Risk Register
Create wiki page `Risk-Register: {Name}` per `skills/risk-register.md`.

### Step 4: Create Sprint Roadmap
Create wiki page `Roadmap: {Name}` per `skills/sprint-roadmap.md`.

### Step 5: Update Charter
Update `Project: {Name}` wiki page:
- Fill Architecture Decisions links (ADRs created so far)
- Link to WBS, Risk Register, Roadmap
- Change status: `Initiating` → `Planning`

### Step 6: Present and Confirm
Show all artifacts to user. Approval transitions to `Executing` (ready for first `/sprint plan`).

## Output

- Wiki pages: `WBS: {Name}`, `Risk-Register: {Name}`, `Roadmap: {Name}`
- Updated: `Project: {Name}` status → Planning
