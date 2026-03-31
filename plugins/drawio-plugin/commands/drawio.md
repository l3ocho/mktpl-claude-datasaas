---
name: drawio
description: draw.io wireframe tools — type /drawio <action> to parse or generate wireframes
---

# /drawio

Wireframe design tools bridging draw.io design files and DMC component scaffolding.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `parse` | `/drawio-plugin:drawio-parse` | Parse .drawio XML → WIREFRAME.md spec + DMC domain file declarations |
| `generate` | `/drawio-plugin:drawio-generate` | Generate .drawio XML from UI description following DMC layer conventions |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/drawio parse path/to/file.drawio`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run — `parse` or `generate`?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names
(e.g., `/drawio-plugin:drawio-parse`)
