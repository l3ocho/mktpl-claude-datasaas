---
name: test
description: Test automation — type /test <action> for commands
---

# /test

Test automation toolkit for unit, integration, and end-to-end testing.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/saas-test-pilot:test-setup` | Setup wizard — detect framework, configure test runner |
| `generate` | `/saas-test-pilot:test-generate` | Generate test cases for functions, classes, or modules |
| `coverage` | `/saas-test-pilot:test-coverage` | Analyze coverage and identify untested paths |
| `fixtures` | `/saas-test-pilot:test-fixtures` | Generate or manage test fixtures and mocks |
| `e2e` | `/saas-test-pilot:test-e2e` | Generate end-to-end test scenarios |
| `run` | `/saas-test-pilot:test-run` | Run tests with formatted output |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/test generate`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/saas-test-pilot:test-generate`)
