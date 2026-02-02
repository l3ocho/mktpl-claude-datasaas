"""
Unit tests for validation tools.
"""
import pytest
from pathlib import Path


@pytest.fixture
def validation_tools():
    """Create ValidationTools instance"""
    from mcp_server.validation_tools import ValidationTools
    return ValidationTools()


@pytest.fixture
def plugin_a(tmp_path):
    """Create first test plugin"""
    plugin_dir = tmp_path / "plugin-a"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()

    readme = plugin_dir / "README.md"
    readme.write_text("""# Plugin A

Test plugin A.

## Commands

| Command | Description |
|---------|-------------|
| `/setup-a` | Setup A |
| `/shared-cmd` | Shared command |

## Tools Summary

### Core (2 tools)
`tool_one`, `tool_two`
""")
    return str(plugin_dir)


@pytest.fixture
def plugin_b(tmp_path):
    """Create second test plugin"""
    plugin_dir = tmp_path / "plugin-b"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()

    readme = plugin_dir / "README.md"
    readme.write_text("""# Plugin B

Test plugin B.

## Commands

| Command | Description |
|---------|-------------|
| `/setup-b` | Setup B |
| `/shared-cmd` | Shared command (conflict!) |

## Tools Summary

### Core (2 tools)
`tool_two`, `tool_three`
""")
    return str(plugin_dir)


@pytest.fixture
def plugin_no_conflict(tmp_path):
    """Create plugin with no conflicts"""
    plugin_dir = tmp_path / "plugin-c"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()

    readme = plugin_dir / "README.md"
    readme.write_text("""# Plugin C

Test plugin C.

## Commands

| Command | Description |
|---------|-------------|
| `/unique-cmd` | Unique command |

## Tools Summary

### Core (1 tool)
`unique_tool`
""")
    return str(plugin_dir)


@pytest.fixture
def claude_md_with_agents(tmp_path):
    """Create CLAUDE.md with agent definitions"""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("""# CLAUDE.md

### Four-Agent Model

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **TestAgent** | Careful | Uses `tool_one`, `tool_two`, `missing_tool` |
| **ValidAgent** | Thorough | Uses `tool_one` only |
| **EmptyAgent** | Unknown | General tasks |
""")
    return str(claude_md)


@pytest.mark.asyncio
async def test_validate_compatibility_command_conflict(validation_tools, plugin_a, plugin_b):
    """Test detection of command name conflicts"""
    result = await validation_tools.validate_compatibility(plugin_a, plugin_b)

    assert "error" not in result
    assert result["compatible"] is False

    # Find the command conflict issue
    error_issues = [i for i in result["issues"] if i["severity"].value == "error"]
    assert len(error_issues) > 0
    assert any("/shared-cmd" in str(i["message"]) for i in error_issues)


@pytest.mark.asyncio
async def test_validate_compatibility_tool_overlap(validation_tools, plugin_a, plugin_b):
    """Test detection of tool name overlaps"""
    result = await validation_tools.validate_compatibility(plugin_a, plugin_b)

    assert "tool_two" in result["shared_tools"]


@pytest.mark.asyncio
async def test_validate_compatibility_unique_tools(validation_tools, plugin_a, plugin_b):
    """Test identification of unique tools per plugin"""
    result = await validation_tools.validate_compatibility(plugin_a, plugin_b)

    assert "tool_one" in result["a_only_tools"]
    assert "tool_three" in result["b_only_tools"]


@pytest.mark.asyncio
async def test_validate_compatibility_no_conflict(validation_tools, plugin_a, plugin_no_conflict):
    """Test compatible plugins"""
    result = await validation_tools.validate_compatibility(plugin_a, plugin_no_conflict)

    assert "error" not in result
    assert result["compatible"] is True


@pytest.mark.asyncio
async def test_validate_compatibility_missing_plugin(validation_tools, plugin_a, tmp_path):
    """Test error when plugin not found"""
    result = await validation_tools.validate_compatibility(
        plugin_a,
        str(tmp_path / "nonexistent")
    )

    assert "error" in result


@pytest.mark.asyncio
async def test_validate_agent_refs_with_missing_tools(validation_tools, claude_md_with_agents, plugin_a):
    """Test detection of missing tool references"""
    result = await validation_tools.validate_agent_refs(
        "TestAgent",
        claude_md_with_agents,
        [plugin_a]
    )

    assert "error" not in result
    assert result["valid"] is False
    assert "missing_tool" in result["tool_refs_missing"]


@pytest.mark.asyncio
async def test_validate_agent_refs_valid_agent(validation_tools, claude_md_with_agents, plugin_a):
    """Test valid agent with all tools found"""
    result = await validation_tools.validate_agent_refs(
        "ValidAgent",
        claude_md_with_agents,
        [plugin_a]
    )

    assert "error" not in result
    assert result["valid"] is True
    assert "tool_one" in result["tool_refs_found"]


@pytest.mark.asyncio
async def test_validate_agent_refs_empty_agent(validation_tools, claude_md_with_agents, plugin_a):
    """Test agent with no tool references"""
    result = await validation_tools.validate_agent_refs(
        "EmptyAgent",
        claude_md_with_agents,
        [plugin_a]
    )

    assert "error" not in result
    # Should have info issue about undocumented references
    info_issues = [i for i in result["issues"] if i["severity"].value == "info"]
    assert len(info_issues) > 0


@pytest.mark.asyncio
async def test_validate_agent_refs_agent_not_found(validation_tools, claude_md_with_agents, plugin_a):
    """Test error when agent not found"""
    result = await validation_tools.validate_agent_refs(
        "NonexistentAgent",
        claude_md_with_agents,
        [plugin_a]
    )

    assert "error" in result
    assert "not found" in result["error"].lower()


@pytest.mark.asyncio
async def test_validate_data_flow_valid(validation_tools, tmp_path):
    """Test data flow validation with valid flow"""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("""# CLAUDE.md

### Four-Agent Model

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **DataAgent** | Analytical | Load with `read_csv`, analyze with `describe`, export with `to_csv` |
""")

    result = await validation_tools.validate_data_flow("DataAgent", str(claude_md))

    assert "error" not in result
    assert result["valid"] is True


@pytest.mark.asyncio
async def test_validate_data_flow_missing_producer(validation_tools, tmp_path):
    """Test data flow with consumer but no producer"""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("""# CLAUDE.md

### Four-Agent Model

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **BadAgent** | Careless | Just runs `describe`, `head`, `tail` without loading |
""")

    result = await validation_tools.validate_data_flow("BadAgent", str(claude_md))

    assert "error" not in result
    # Should have warning about missing producer
    warning_issues = [i for i in result["issues"] if i["severity"].value == "warning"]
    assert len(warning_issues) > 0


# --- Workflow Integration Tests ---

@pytest.fixture
def domain_plugin_complete(tmp_path):
    """Create a complete domain plugin with gate, review, and advisory agent"""
    plugin_dir = tmp_path / "viz-platform"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()
    (plugin_dir / "commands").mkdir()
    (plugin_dir / "agents").mkdir()

    # Gate command with PASS/FAIL pattern
    gate_cmd = plugin_dir / "commands" / "design-gate.md"
    gate_cmd.write_text("""# /design-gate

Binary pass/fail validation gate for design system compliance.

## Output

- **PASS**: All design system checks passed
- **FAIL**: Design system violations detected
""")

    # Review command
    review_cmd = plugin_dir / "commands" / "design-review.md"
    review_cmd.write_text("""# /design-review

Comprehensive design system audit.
""")

    # Advisory agent
    agent = plugin_dir / "agents" / "design-reviewer.md"
    agent.write_text("""# design-reviewer

Design system compliance auditor.

Handles issues with `Domain/Viz` label.
""")

    return str(plugin_dir)


@pytest.fixture
def domain_plugin_missing_gate(tmp_path):
    """Create domain plugin with review and agent but no gate command"""
    plugin_dir = tmp_path / "data-platform"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()
    (plugin_dir / "commands").mkdir()
    (plugin_dir / "agents").mkdir()

    # Review command (but no gate)
    review_cmd = plugin_dir / "commands" / "data-review.md"
    review_cmd.write_text("""# /data-review

Data integrity audit.
""")

    # Advisory agent
    agent = plugin_dir / "agents" / "data-advisor.md"
    agent.write_text("""# data-advisor

Data integrity advisor for Domain/Data issues.
""")

    return str(plugin_dir)


@pytest.fixture
def domain_plugin_minimal(tmp_path):
    """Create minimal plugin with no commands or agents"""
    plugin_dir = tmp_path / "minimal-plugin"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()

    readme = plugin_dir / "README.md"
    readme.write_text("# Minimal Plugin\n\nNo commands or agents.")

    return str(plugin_dir)


@pytest.mark.asyncio
async def test_validate_workflow_integration_complete(validation_tools, domain_plugin_complete):
    """Test complete domain plugin returns valid with all interfaces found"""
    result = await validation_tools.validate_workflow_integration(
        domain_plugin_complete,
        "Domain/Viz"
    )

    assert "error" not in result
    assert result["valid"] is True
    assert result["gate_command_found"] is True
    assert result["review_command_found"] is True
    assert result["advisory_agent_found"] is True
    assert len(result["issues"]) == 0


@pytest.mark.asyncio
async def test_validate_workflow_integration_missing_gate(validation_tools, domain_plugin_missing_gate):
    """Test plugin missing gate command returns invalid with ERROR"""
    result = await validation_tools.validate_workflow_integration(
        domain_plugin_missing_gate,
        "Domain/Data"
    )

    assert "error" not in result
    assert result["valid"] is False
    assert result["gate_command_found"] is False
    assert result["review_command_found"] is True
    assert result["advisory_agent_found"] is True

    # Should have one ERROR for missing gate
    error_issues = [i for i in result["issues"] if i["severity"].value == "error"]
    assert len(error_issues) == 1
    assert "gate" in error_issues[0]["message"].lower()


@pytest.mark.asyncio
async def test_validate_workflow_integration_minimal(validation_tools, domain_plugin_minimal):
    """Test minimal plugin returns invalid with multiple issues"""
    result = await validation_tools.validate_workflow_integration(
        domain_plugin_minimal,
        "Domain/Test"
    )

    assert "error" not in result
    assert result["valid"] is False
    assert result["gate_command_found"] is False
    assert result["review_command_found"] is False
    assert result["advisory_agent_found"] is False

    # Should have one ERROR (gate) and two WARNINGs (review, agent)
    error_issues = [i for i in result["issues"] if i["severity"].value == "error"]
    warning_issues = [i for i in result["issues"] if i["severity"].value == "warning"]
    assert len(error_issues) == 1
    assert len(warning_issues) == 2


@pytest.mark.asyncio
async def test_validate_workflow_integration_nonexistent_plugin(validation_tools, tmp_path):
    """Test error when plugin directory doesn't exist"""
    result = await validation_tools.validate_workflow_integration(
        str(tmp_path / "nonexistent"),
        "Domain/Test"
    )

    assert "error" in result
    assert "not found" in result["error"].lower()


# --- Gate Contract Version Tests ---

@pytest.fixture
def domain_plugin_with_contract(tmp_path):
    """Create domain plugin with gate_contract: v1 in frontmatter"""
    plugin_dir = tmp_path / "viz-platform-versioned"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()
    (plugin_dir / "commands").mkdir()
    (plugin_dir / "agents").mkdir()

    # Gate command with gate_contract in frontmatter
    gate_cmd = plugin_dir / "commands" / "design-gate.md"
    gate_cmd.write_text("""---
description: Design system compliance gate (pass/fail)
gate_contract: v1
---

# /design-gate

Binary pass/fail validation gate for design system compliance.

## Output

- **PASS**: All design system checks passed
- **FAIL**: Design system violations detected
""")

    # Review command
    review_cmd = plugin_dir / "commands" / "design-review.md"
    review_cmd.write_text("""# /design-review

Comprehensive design system audit.
""")

    # Advisory agent
    agent = plugin_dir / "agents" / "design-reviewer.md"
    agent.write_text("""# design-reviewer

Design system compliance auditor for Domain/Viz issues.
""")

    return str(plugin_dir)


@pytest.mark.asyncio
async def test_validate_workflow_contract_match(validation_tools, domain_plugin_with_contract):
    """Test that matching expected_contract produces no warning"""
    result = await validation_tools.validate_workflow_integration(
        domain_plugin_with_contract,
        "Domain/Viz",
        expected_contract="v1"
    )

    assert "error" not in result
    assert result["valid"] is True
    assert result["gate_contract"] == "v1"

    # Should have no warnings about contract mismatch
    warning_issues = [i for i in result["issues"] if i["severity"].value == "warning"]
    contract_warnings = [i for i in warning_issues if "contract" in i["message"].lower()]
    assert len(contract_warnings) == 0


@pytest.mark.asyncio
async def test_validate_workflow_contract_mismatch(validation_tools, domain_plugin_with_contract):
    """Test that mismatched expected_contract produces WARNING"""
    result = await validation_tools.validate_workflow_integration(
        domain_plugin_with_contract,
        "Domain/Viz",
        expected_contract="v2"  # Gate has v1
    )

    assert "error" not in result
    assert result["valid"] is True  # Contract mismatch doesn't affect validity
    assert result["gate_contract"] == "v1"

    # Should have warning about contract mismatch
    warning_issues = [i for i in result["issues"] if i["severity"].value == "warning"]
    contract_warnings = [i for i in warning_issues if "contract" in i["message"].lower()]
    assert len(contract_warnings) == 1
    assert "mismatch" in contract_warnings[0]["message"].lower()
    assert "v1" in contract_warnings[0]["message"]
    assert "v2" in contract_warnings[0]["message"]


@pytest.mark.asyncio
async def test_validate_workflow_no_contract(validation_tools, domain_plugin_complete):
    """Test that missing gate_contract produces INFO suggestion"""
    result = await validation_tools.validate_workflow_integration(
        domain_plugin_complete,
        "Domain/Viz"
    )

    assert "error" not in result
    assert result["valid"] is True
    assert result["gate_contract"] is None

    # Should have info issue about missing contract
    info_issues = [i for i in result["issues"] if i["severity"].value == "info"]
    contract_info = [i for i in info_issues if "contract" in i["message"].lower()]
    assert len(contract_info) == 1
    assert "does not declare" in contract_info[0]["message"].lower()
