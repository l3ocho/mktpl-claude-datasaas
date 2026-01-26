"""
Unit tests for parse tools.
"""
import pytest
from pathlib import Path


@pytest.fixture
def parse_tools():
    """Create ParseTools instance"""
    from mcp_server.parse_tools import ParseTools
    return ParseTools()


@pytest.fixture
def sample_readme(tmp_path):
    """Create a sample README.md for testing"""
    readme = tmp_path / "README.md"
    readme.write_text("""# Test Plugin

A test plugin for validation.

## Features

- **Feature One**: Does something
- **Feature Two**: Does something else

## Commands

| Command | Description |
|---------|-------------|
| `/test-cmd` | Test command |
| `/another-cmd` | Another test command |

## Agents

| Agent | Description |
|-------|-------------|
| `test-agent` | A test agent |

## Tools Summary

### Category A (3 tools)
`tool_a`, `tool_b`, `tool_c`

### Category B (2 tools)
`tool_d`, `tool_e`
""")
    return str(tmp_path)


@pytest.fixture
def sample_claude_md(tmp_path):
    """Create a sample CLAUDE.md for testing"""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("""# CLAUDE.md

## Project Overview

### Four-Agent Model (test)

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **Planner** | Thoughtful | Planning via `create_issue`, `search_lessons` |
| **Executor** | Focused | Implementation via `write`, `edit` |

## Workflow

1. Planner creates issues
2. Executor implements code
""")
    return str(claude_md)


@pytest.mark.asyncio
async def test_parse_plugin_interface_basic(parse_tools, sample_readme):
    """Test basic plugin interface parsing"""
    result = await parse_tools.parse_plugin_interface(sample_readme)

    assert "error" not in result
    # Plugin name extraction strips "Plugin" suffix
    assert result["plugin_name"] == "Test"
    assert "A test plugin" in result["description"]


@pytest.mark.asyncio
async def test_parse_plugin_interface_commands(parse_tools, sample_readme):
    """Test command extraction from README"""
    result = await parse_tools.parse_plugin_interface(sample_readme)

    commands = result["commands"]
    assert len(commands) == 2
    assert commands[0]["name"] == "/test-cmd"
    assert commands[1]["name"] == "/another-cmd"


@pytest.mark.asyncio
async def test_parse_plugin_interface_agents(parse_tools, sample_readme):
    """Test agent extraction from README"""
    result = await parse_tools.parse_plugin_interface(sample_readme)

    agents = result["agents"]
    assert len(agents) == 1
    assert agents[0]["name"] == "test-agent"


@pytest.mark.asyncio
async def test_parse_plugin_interface_tools(parse_tools, sample_readme):
    """Test tool extraction from README"""
    result = await parse_tools.parse_plugin_interface(sample_readme)

    tools = result["tools"]
    tool_names = [t["name"] for t in tools]
    assert "tool_a" in tool_names
    assert "tool_b" in tool_names
    assert "tool_e" in tool_names
    assert len(tools) >= 5


@pytest.mark.asyncio
async def test_parse_plugin_interface_categories(parse_tools, sample_readme):
    """Test tool category extraction"""
    result = await parse_tools.parse_plugin_interface(sample_readme)

    categories = result["tool_categories"]
    assert "Category A" in categories
    assert "Category B" in categories
    assert "tool_a" in categories["Category A"]


@pytest.mark.asyncio
async def test_parse_plugin_interface_features(parse_tools, sample_readme):
    """Test feature extraction"""
    result = await parse_tools.parse_plugin_interface(sample_readme)

    features = result["features"]
    assert "Feature One" in features
    assert "Feature Two" in features


@pytest.mark.asyncio
async def test_parse_plugin_interface_not_found(parse_tools, tmp_path):
    """Test error when README not found"""
    result = await parse_tools.parse_plugin_interface(str(tmp_path / "nonexistent"))

    assert "error" in result
    assert "not found" in result["error"].lower()


@pytest.mark.asyncio
async def test_parse_claude_md_agents(parse_tools, sample_claude_md):
    """Test agent extraction from CLAUDE.md"""
    result = await parse_tools.parse_claude_md_agents(sample_claude_md)

    assert "error" not in result
    assert result["agent_count"] == 2

    agents = result["agents"]
    agent_names = [a["name"] for a in agents]
    assert "Planner" in agent_names
    assert "Executor" in agent_names


@pytest.mark.asyncio
async def test_parse_claude_md_tool_refs(parse_tools, sample_claude_md):
    """Test tool reference extraction from agents"""
    result = await parse_tools.parse_claude_md_agents(sample_claude_md)

    agents = {a["name"]: a for a in result["agents"]}
    planner = agents["Planner"]

    assert "create_issue" in planner["tool_refs"]
    assert "search_lessons" in planner["tool_refs"]


@pytest.mark.asyncio
async def test_parse_claude_md_not_found(parse_tools, tmp_path):
    """Test error when CLAUDE.md not found"""
    result = await parse_tools.parse_claude_md_agents(str(tmp_path / "CLAUDE.md"))

    assert "error" in result
    assert "not found" in result["error"].lower()


@pytest.mark.asyncio
async def test_parse_plugin_with_direct_file(parse_tools, sample_readme):
    """Test parsing with direct file path instead of directory"""
    readme_path = Path(sample_readme) / "README.md"
    result = await parse_tools.parse_plugin_interface(str(readme_path))

    assert "error" not in result
    # Plugin name extraction strips "Plugin" suffix
    assert result["plugin_name"] == "Test"
