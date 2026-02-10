---
name: debug-mcp test
description: Test a specific MCP tool call by invoking it and displaying the result
---

# /debug-mcp test

Test a specific MCP tool by invoking it with sample parameters.

## Skills to Load

- `skills/visual-header.md`
- `skills/mcp-protocol.md`

## Agent

Delegate to `agents/mcp-debugger.md`.

## Usage

```
/debug-mcp test <server_name> <tool_name> [--params=<json>]
```

**Arguments:**
- `server_name` - Name of the MCP server from .mcp.json
- `tool_name` - Name of the tool to invoke
- `--params` - JSON object with tool parameters (optional)

## Instructions

Execute `skills/visual-header.md` with context "Tool Test".

### Phase 1: Validate Inputs

1. Read `.mcp.json` and verify the server exists
2. Check if the server is healthy (run quick executable check)
3. If tool_name is not provided, list available tools for the server and ask user to select

### Phase 2: Tool Discovery

1. Parse the server source code to find the tool definition
2. Extract the tool's `inputSchema` (parameters, types, required fields)
3. Display the schema to the user:
   ```
   ## Tool: list_issues
   Server: gitea

   Parameters:
   - state (string, optional): "open", "closed", "all" [default: "open"]
   - labels (array[string], optional): Filter by labels
   - repo (string, optional): Repository name
   ```

### Phase 3: Parameter Preparation

1. If `--params` provided, validate against the tool's inputSchema
2. If no params provided and tool has required params, ask user for values
3. If no params and all optional, invoke with defaults

### Phase 4: Invocation

Invoke the MCP tool using the available MCP tool functions:
1. Call the tool with prepared parameters
2. Capture the response
3. Measure response time

### Phase 5: Result Display

```
## Test Result

### Request
- Server: gitea
- Tool: list_issues
- Params: {"state": "open", "repo": "mktpl-claude-datasaas"}

### Response
- Status: Success
- Time: 245ms
- Result:
  [formatted JSON response, truncated if large]

### Schema Validation
- All required params provided: YES
- Response type matches expected: YES
```

### Error Handling

If the tool call fails, apply `skills/mcp-protocol.md` error patterns:

```
### Error
- Type: ConnectionRefused
- Message: Could not connect to MCP server
- Likely Cause: Server not running or venv broken
- Fix: Run /debug-mcp status to diagnose
```

## User Request

$ARGUMENTS
