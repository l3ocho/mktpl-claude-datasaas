# Visual Header Skill

Standard visual header for cmdb-assistant commands.

## Header Template

```
+----------------------------------------------------------------------+
|  CMDB-ASSISTANT - [Context]                                          |
+----------------------------------------------------------------------+
```

## Context Values by Command

| Command | Context |
|---------|---------|
| `/cmdb search` | Search |
| `/cmdb device` | Device Management |
| `/cmdb ip` | IP Management |
| `/cmdb site` | Site Management |
| `/cmdb audit` | Data Quality Audit |
| `/cmdb register` | Machine Registration |
| `/cmdb sync` | Machine Sync |
| `/cmdb topology` | Topology |
| `/cmdb change-audit` | Change Audit |
| `/cmdb ip-conflicts` | IP Conflict Detection |
| `/cmdb setup` | Setup Wizard |
| Agent mode | Infrastructure Management |

## Usage

Display header at the start of every command response before proceeding with the operation.
