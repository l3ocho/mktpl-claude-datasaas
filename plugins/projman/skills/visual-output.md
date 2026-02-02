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
| `/sprint-status` | 📊 Chart | STATUS |
| `/setup` | ⚙️ Gear | SETUP |
| `/debug` | 🐛 Bug | DEBUG |
| `/labels-sync` | 🏷️ Label | LABELS |
| `/suggest-version` | 📦 Package | VERSION |
| `/proposal-status` | 📋 Clipboard | PROPOSALS |
| `/test` | 🧪 Flask | TEST |
| `/rfc` | 📄 Document | RFC [Sub-Command] |

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
