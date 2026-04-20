---
name: design component
description: Validate DMC component usage against the design contract
skills:
  - skills/dmc-components.md
  - skills/mcp-tools-reference.md
---

# /design component

Validate Dash Mantine Components usage against the design contract.

## Arguments

`$ARGUMENTS` — component name or file path

## Steps

1. If component name given: use `get_component_props` MCP tool to get valid props
2. If file path given: read file and validate all DMC component usages
3. Use `validate_component` MCP tool for schema validation
4. Report any props that violate the contract
5. Suggest corrections
