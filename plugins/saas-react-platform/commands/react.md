---
name: react
description: React development toolkit — type /react <action> for commands
---

# /react

React frontend development toolkit with component scaffolding, routing, state management, and anti-pattern detection.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/saas-react-platform:react-setup` | Setup wizard for React project detection and configuration |
| `component` | `/saas-react-platform:react-component` | Scaffold component with props, types, and tests |
| `route` | `/saas-react-platform:react-route` | Add route with page component and error boundary |
| `state` | `/saas-react-platform:react-state` | Set up state management pattern (Context, Zustand, Redux Toolkit) |
| `hook` | `/saas-react-platform:react-hook` | Generate custom hook with types and tests |
| `lint` | `/saas-react-platform:react-lint` | Validate component tree and detect anti-patterns |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/react component`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/saas-react-platform:react-component`)
