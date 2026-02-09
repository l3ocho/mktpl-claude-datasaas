---
name: test
description: Test automation — type /test <action> for commands
---

# /test

Test automation toolkit for unit, integration, and end-to-end testing.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/test setup` | Setup wizard — detect framework, configure test runner |
| `/test generate` | Generate test cases for functions, classes, or modules |
| `/test coverage` | Analyze coverage and identify untested paths |
| `/test fixtures` | Generate or manage test fixtures and mocks |
| `/test e2e` | Generate end-to-end test scenarios |
| `/test run` | Run tests with formatted output |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
