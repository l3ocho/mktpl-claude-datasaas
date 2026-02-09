---
name: react
description: React development toolkit — type /react <action> for commands
---

# /react

React frontend development toolkit with component scaffolding, routing, state management, and anti-pattern detection.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/react setup` | Setup wizard for React project detection and configuration |
| `/react component` | Scaffold component with props, types, and tests |
| `/react route` | Add route with page component and error boundary |
| `/react state` | Set up state management pattern (Context, Zustand, Redux Toolkit) |
| `/react hook` | Generate custom hook with types and tests |
| `/react lint` | Validate component tree and detect anti-patterns |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
