---
name: project
description: Project lifecycle management — type /project <action> for commands
---

# /project

Project lifecycle management from concept to MVP.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `initiation` | `/projman:project-initiation` | Analyze source, create charter, decompose into epics |
| `plan` | `/projman:project-plan` | Create WBS, risk register, sprint roadmap |
| `status` | `/projman:project-status` | Full project hierarchy view |
| `close` | `/projman:project-close` | Retrospective, lessons learned, archive |

## Usage

```
/project initiation <source-path-or-description>
/project plan <project-name>
/project status <project-name>
/project close <project-name>
```

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/project initiation`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/projman:project-initiation`)
