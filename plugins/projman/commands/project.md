---
name: project
description: Project lifecycle management — type /project <action> for commands
---

# /project

Project lifecycle management from concept to MVP.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/project initiation` | Analyze source, create charter, decompose into epics |
| `/project plan` | Create WBS, risk register, sprint roadmap |
| `/project status` | Full project hierarchy view |
| `/project close` | Retrospective, lessons learned, archive |

## Usage

```
/project initiation <source-path-or-description>
/project plan <project-name>
/project status <project-name>
/project close <project-name>
```

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
