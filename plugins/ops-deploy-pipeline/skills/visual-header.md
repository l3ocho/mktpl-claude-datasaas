# Visual Header Skill

Standard visual header for ops-deploy-pipeline commands.

## Header Template

```
+----------------------------------------------------------------------+
|  DEPLOY-PIPELINE - [Context]                                          |
+----------------------------------------------------------------------+
```

## Context Values by Command

| Command | Context |
|---------|---------|
| `/deploy setup` | Setup Wizard |
| `/deploy generate` | Config Generation |
| `/deploy validate` | Config Validation |
| `/deploy env` | Environment Management |
| `/deploy check` | Pre-Deployment Check |
| `/deploy rollback` | Rollback Planning |
| Agent mode | Deployment Management |

## Usage

Display header at the start of every command response before proceeding with the operation.
