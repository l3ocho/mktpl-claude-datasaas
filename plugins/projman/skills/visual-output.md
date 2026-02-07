---
name: visual-output
description: Standard visual formatting for projman commands and agents
---

# Visual Output Standards

## Purpose

Single source of truth for all projman visual headers, progress blocks, and verdict formats. All agents and commands reference this skill instead of defining their own templates.

---

## Plugin Header (Double-Line)

Projman uses the double-line box drawing header style with emoji phase indicators.

### Agent Headers

```
+----------------------------------------------------------------------+
|  PROJMAN                                                             |
|  [Phase Emoji] [PHASE NAME]                                          |
|  [Context Line]                                                      |
+----------------------------------------------------------------------+
```

### Phase Registry

| Agent | Phase Emoji | Phase Name | Context |
|-------|-------------|------------|---------|
| Planner | 🎯 Target | PLANNING | Sprint Name or Goal |
| Orchestrator | ⚡ Lightning | EXECUTION | Sprint Name |
| Executor | 🔧 Wrench | IMPLEMENTING | Issue Title |
| Code Reviewer | 🔍 Magnifier | REVIEW | Sprint Name |

### Command Headers (Non-Agent)

For commands that don't invoke a specific agent phase:

| Command | Phase Emoji | Phase Name |
|---------|-------------|------------|
| `/sprint status` | 📊 Chart | STATUS |
| `/projman setup` | ⚙️ Gear | SETUP |
| `/labels sync` | 🏷️ Label | LABELS |
| `/sprint test` | 🧪 Flask | TEST |
| `/rfc` | 📄 Document | RFC [Sub-Command] |
| `/project` | 📋 Clipboard | PROJECT [Sub-Command] |
| `/adr` | 📐 Ruler | ADR [Sub-Command] |
| `/hygiene check` | 🧹 Broom | HYGIENE |
| `/cv status` | ✅ Check | CV STATUS |

---

## Progress Block

Used by orchestrator during sprint execution:

```
+-- Sprint Progress -------------------------------------------------------+
|  [Sprint Name]                                                           |
|  [Progress bar] XX% complete                                             |
|  Done: X    Active: X    Pending: X                                      |
+--------------------------------------------------------------------------+
```

---

## Sprint Close Summary

```
+----------------------------------------------------------------------+
|  PROJMAN                                                             |
|  Finish Flag CLOSING                                                 |
|  [Sprint Name]                                                       |
+----------------------------------------------------------------------+
```

---

## Gate Verdict Format

For domain gate results displayed by orchestrator:

```
+-- Domain Gate: [Viz/Data] -----------------------------------------------+
|  Status: PASS / FAIL                                                     |
|  [Details if FAIL]                                                       |
+--------------------------------------------------------------------------+
```

---

## Status Indicators

| Indicator | Meaning |
|-----------|---------|
| Check | Complete / Pass |
| X | Failed / Blocked |
| Hourglass | In progress |
| Empty box | Pending / Not started |
| Warning | Warning |

---

## Token Budget Report

Displayed at end of planning and closing phases:

```
+-- Token Budget Report -----------------------------------------------+
|  Phase: [PHASE NAME]                                                 |
|  Sprint: [Sprint Name]                                               |
+----------------------------------------------------------------------+
|  MCP Overhead: ~XX,XXX tk                                            |
|  Phase Cost:   ~X,XXX tk  (skills: N, agent: model)                 |
|  Est. Total:   ~XX,XXX tk (~XX% of budget)                          |
+----------------------------------------------------------------------+
```

See `skills/token-budget-report.md` for full format and estimation model.
