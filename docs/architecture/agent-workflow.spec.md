# Agent Workflow - Draw.io Specification

**Target File:** `docs/architecture/agent-workflow.drawio`

**Purpose:** Shows when Planner, Orchestrator, and Executor agents trigger during sprint lifecycle.

**Diagram Type:** Swimlane / Sequence Diagram

---

## SWIMLANES

| ID | Label | Color | Position |
|----|-------|-------|----------|
| user-lane | User | #E3F2FD | 1 (leftmost) |
| planner-lane | Planner Agent | #4A90D9 | 2 |
| orchestrator-lane | Orchestrator Agent | #7CB342 | 3 |
| executor-lane | Executor Agent | #FF9800 | 4 |
| gitea-lane | Gitea | #9E9E9E | 5 |
| wikijs-lane | Wiki.js | #9E9E9E | 6 (rightmost) |

---

## PHASE 1: SPRINT PLANNING

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p1-start | /sprint-plan | rounded-rect | user-lane | 1 |
| p1-activate | Planner Activates | rectangle | planner-lane | 2 |
| p1-search-lessons | Search Lessons Learned | rectangle | planner-lane | 3 |
| p1-wikijs-query | Query Past Lessons | rectangle | wikijs-lane | 4 |
| p1-return-lessons | Return Relevant Lessons | rectangle | planner-lane | 5 |
| p1-clarify | Ask Clarifying Questions | diamond | planner-lane | 6 |
| p1-user-answers | Provide Answers | rectangle | user-lane | 7 |
| p1-create-issues | Create Issues with Labels | rectangle | planner-lane | 8 |
| p1-gitea-create | Store Issues | rectangle | gitea-lane | 9 |
| p1-plan-complete | Planning Complete | rounded-rect | planner-lane | 10 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p1-start | p1-activate | invokes | solid |
| p1-activate | p1-search-lessons | | solid |
| p1-search-lessons | p1-wikijs-query | GraphQL search | solid |
| p1-wikijs-query | p1-return-lessons | lessons data | dashed |
| p1-return-lessons | p1-clarify | | solid |
| p1-clarify | p1-user-answers | questions | solid |
| p1-user-answers | p1-clarify | answers | dashed |
| p1-clarify | p1-create-issues | | solid |
| p1-create-issues | p1-gitea-create | REST API | solid |
| p1-gitea-create | p1-plan-complete | confirm | dashed |

---

## PHASE 2: SPRINT EXECUTION

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p2-start | /sprint-start | rounded-rect | user-lane | 11 |
| p2-orch-activate | Orchestrator Activates | rectangle | orchestrator-lane | 12 |
| p2-fetch-issues | Fetch Sprint Issues | rectangle | orchestrator-lane | 13 |
| p2-gitea-list | List Open Issues | rectangle | gitea-lane | 14 |
| p2-sequence | Sequence Work | rectangle | orchestrator-lane | 15 |
| p2-dispatch | Dispatch Task | rectangle | orchestrator-lane | 16 |
| p2-exec-activate | Executor Activates | rectangle | executor-lane | 17 |
| p2-implement | Implement Task | rectangle | executor-lane | 18 |
| p2-update-status | Update Issue Status | rectangle | executor-lane | 19 |
| p2-gitea-update | Update Issue | rectangle | gitea-lane | 20 |
| p2-report | Report Completion | rectangle | executor-lane | 21 |
| p2-loop | More Tasks? | diamond | orchestrator-lane | 22 |
| p2-exec-complete | Execution Complete | rounded-rect | orchestrator-lane | 23 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p2-start | p2-orch-activate | invokes | solid |
| p2-orch-activate | p2-fetch-issues | | solid |
| p2-fetch-issues | p2-gitea-list | REST API | solid |
| p2-gitea-list | p2-sequence | issues data | dashed |
| p2-sequence | p2-dispatch | | solid |
| p2-dispatch | p2-exec-activate | execution prompt | solid |
| p2-exec-activate | p2-implement | | solid |
| p2-implement | p2-update-status | | solid |
| p2-update-status | p2-gitea-update | REST API | solid |
| p2-gitea-update | p2-report | confirm | dashed |
| p2-report | p2-loop | | solid |
| p2-loop | p2-dispatch | yes | solid |
| p2-loop | p2-exec-complete | no | solid |

---

## PHASE 3: SPRINT CLOSE

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p3-start | /sprint-close | rounded-rect | user-lane | 24 |
| p3-orch-activate | Orchestrator Activates | rectangle | orchestrator-lane | 25 |
| p3-review | Review Sprint | rectangle | orchestrator-lane | 26 |
| p3-gitea-status | Get Final Status | rectangle | gitea-lane | 27 |
| p3-capture | Capture Lessons Learned | rectangle | orchestrator-lane | 28 |
| p3-user-input | Confirm Lessons | diamond | user-lane | 29 |
| p3-create-wiki | Create Wiki Pages | rectangle | orchestrator-lane | 30 |
| p3-wikijs-create | Store Lessons | rectangle | wikijs-lane | 31 |
| p3-close-issues | Close Issues | rectangle | orchestrator-lane | 32 |
| p3-gitea-close | Mark Closed | rectangle | gitea-lane | 33 |
| p3-complete | Sprint Closed | rounded-rect | orchestrator-lane | 34 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p3-start | p3-orch-activate | invokes | solid |
| p3-orch-activate | p3-review | | solid |
| p3-review | p3-gitea-status | REST API | solid |
| p3-gitea-status | p3-capture | status data | dashed |
| p3-capture | p3-user-input | proposed lessons | solid |
| p3-user-input | p3-create-wiki | confirmed | solid |
| p3-create-wiki | p3-wikijs-create | GraphQL mutation | solid |
| p3-wikijs-create | p3-close-issues | confirm | dashed |
| p3-close-issues | p3-gitea-close | REST API | solid |
| p3-gitea-close | p3-complete | confirm | dashed |

---

## LAYOUT NOTES

```
+--------+------------+---------------+------------+--------+----------+
|  User  |  Planner   | Orchestrator  |  Executor  | Gitea  | Wiki.js  |
+--------+------------+---------------+------------+--------+----------+
|        |            |               |            |        |          |
| PHASE 1: SPRINT PLANNING                                             |
|---------------------------------------------------------------------+
|  O     |            |               |            |        |          |
|  |     |            |               |            |        |          |
|  +---->| O          |               |            |        |          |
|        | |          |               |            |        |          |
|        | +----------|---------------|------------|------->| O        |
|        | |<---------|---------------|------------|--------+ |        |
|        | |          |               |            |        |          |
|        | O<>        |               |            |        |          |
|  O<--->+ |          |               |            |        |          |
|        | |          |               |            |        |          |
|        | +----------|---------------|----------->| O      |          |
|        | O          |               |            |        |          |
|        |            |               |            |        |          |
|---------------------------------------------------------------------+
| PHASE 2: SPRINT EXECUTION                                            |
|---------------------------------------------------------------------+
|  O     |            |               |            |        |          |
|  |     |            |               |            |        |          |
|  +-----|----------->| O             |            |        |          |
|        |            | |             |            |        |          |
|        |            | +-------------|----------->| O      |          |
|        |            | |<------------|------------+ |      |          |
|        |            | |             |            |        |          |
|        |            | +------------>| O          |        |          |
|        |            |               | |          |        |          |
|        |            |               | +--------->| O      |          |
|        |            |               | |<---------+ |      |          |
|        |            | O<------------+ |          |        |          |
|        |            | |             |            |        |          |
|        |            | O (loop)      |            |        |          |
|        |            |               |            |        |          |
|---------------------------------------------------------------------+
| PHASE 3: SPRINT CLOSE                                                |
|---------------------------------------------------------------------+
|  O     |            |               |            |        |          |
|  |     |            |               |            |        |          |
|  +-----|----------->| O             |            |        |          |
|        |            | +-------------|----------->| O      |          |
|        |            | |<------------|------------+ |      |          |
|        |            | |             |            |        |          |
|  O<----|-----------<+ |             |            |        |          |
|  +-----|----------->| |             |            |        |          |
|        |            | +-------------|------------|------->| O        |
|        |            | |<------------|------------|--------+ |        |
|        |            | +-------------|----------->| O      |          |
|        |            | O             |            |        |          |
+--------+------------+---------------+------------+--------+----------+
```

---

## COLOR LEGEND

| Color | Hex | Meaning |
|-------|-----|---------|
| Light Blue | #E3F2FD | User actions |
| Blue | #4A90D9 | Planner Agent |
| Green | #7CB342 | Orchestrator Agent |
| Orange | #FF9800 | Executor Agent |
| Gray | #9E9E9E | External Services |

---

## SHAPE LEGEND

| Shape | Meaning |
|-------|---------|
| Rounded Rectangle | Start/End points (commands) |
| Rectangle | Process/Action |
| Diamond | Decision point |
| Cylinder | Data store (in component map) |

---

## ARROW LEGEND

| Style | Meaning |
|-------|---------|
| Solid | Action/Request |
| Dashed | Response/Data return |
