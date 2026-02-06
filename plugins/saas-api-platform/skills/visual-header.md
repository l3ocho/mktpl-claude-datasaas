---
name: visual-header
description: Standard header format for API platform commands and agents
---

# Visual Header

## Standard Format

Display at the start of every command execution:

```
+----------------------------------------------------------------------+
|  API-PLATFORM - [Command Name]                                       |
+----------------------------------------------------------------------+
```

## Command Headers

| Command | Header Text |
|---------|-------------|
| api-setup | Setup Wizard |
| api-scaffold | Scaffold |
| api-validate | Validate |
| api-docs | Docs |
| api-test-routes | Test Routes |
| api-middleware | Middleware |

## Summary Box Format

For completion summaries:

```
+============================================================+
|            API-PLATFORM [OPERATION] COMPLETE                |
+============================================================+
| Component:         [Status]                                |
| Component:         [Status]                                |
+============================================================+
```

## Status Indicators

- Success: `[check]` or `Ready`
- Warning: `[!]` or `Partial`
- Failure: `[X]` or `Failed`
- New file: `[+]`
- Modified file: `[~]`
- Deleted file: `[-]`
