---
name: clarity
description: Prompt optimization and requirement clarification — type /clarity <action> for commands
---

# /clarity

Prompt optimization and requirement clarification with ND-friendly accommodations.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `clarify` | `/clarity-assist:clarity-clarify` | Full 4-D methodology for complex requests |
| `quick-clarify` | `/clarity-assist:clarity-quick-clarify` | Rapid mode for simple disambiguation |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/clarity clarify`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/clarity-assist:clarity-clarify`)
