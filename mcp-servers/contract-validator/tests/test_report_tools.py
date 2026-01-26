"""
Unit tests for report tools.
"""
import pytest
from pathlib import Path


@pytest.fixture
def report_tools():
    """Create ReportTools instance"""
    from mcp_server.report_tools import ReportTools
    return ReportTools()


@pytest.fixture
def sample_marketplace(tmp_path):
    """Create a sample marketplace structure"""
    import json

    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    # Plugin 1
    plugin1 = plugins_dir / "plugin-one"
    plugin1.mkdir()
    plugin1_meta = plugin1 / ".claude-plugin"
    plugin1_meta.mkdir()
    (plugin1_meta / "plugin.json").write_text(json.dumps({"name": "plugin-one"}))
    (plugin1 / "README.md").write_text("""# plugin-one

First test plugin.

## Commands

| Command | Description |
|---------|-------------|
| `/cmd-one` | Command one |

## Tools Summary

### Tools (2 tools)
`tool_a`, `tool_b`
""")

    # Plugin 2
    plugin2 = plugins_dir / "plugin-two"
    plugin2.mkdir()
    plugin2_meta = plugin2 / ".claude-plugin"
    plugin2_meta.mkdir()
    (plugin2_meta / "plugin.json").write_text(json.dumps({"name": "plugin-two"}))
    (plugin2 / "README.md").write_text("""# plugin-two

Second test plugin.

## Commands

| Command | Description |
|---------|-------------|
| `/cmd-two` | Command two |

## Tools Summary

### Tools (2 tools)
`tool_c`, `tool_d`
""")

    # Plugin 3 (with conflict)
    plugin3 = plugins_dir / "plugin-three"
    plugin3.mkdir()
    plugin3_meta = plugin3 / ".claude-plugin"
    plugin3_meta.mkdir()
    (plugin3_meta / "plugin.json").write_text(json.dumps({"name": "plugin-three"}))
    (plugin3 / "README.md").write_text("""# plugin-three

Third test plugin with conflict.

## Commands

| Command | Description |
|---------|-------------|
| `/cmd-one` | Conflicting command |

## Tools Summary

### Tools (1 tool)
`tool_e`
""")

    return str(tmp_path)


@pytest.fixture
def marketplace_no_plugins(tmp_path):
    """Create marketplace with no plugins"""
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    return str(tmp_path)


@pytest.fixture
def marketplace_no_dir(tmp_path):
    """Create path without plugins directory"""
    return str(tmp_path)


@pytest.mark.asyncio
async def test_generate_report_json_format(report_tools, sample_marketplace):
    """Test JSON format report generation"""
    result = await report_tools.generate_compatibility_report(
        sample_marketplace, "json"
    )

    assert "error" not in result
    assert "generated_at" in result
    assert "summary" in result
    assert "plugins" in result
    assert result["summary"]["total_plugins"] == 3


@pytest.mark.asyncio
async def test_generate_report_markdown_format(report_tools, sample_marketplace):
    """Test markdown format report generation"""
    result = await report_tools.generate_compatibility_report(
        sample_marketplace, "markdown"
    )

    assert "error" not in result
    assert "report" in result
    assert "# Contract Validation Report" in result["report"]
    assert "## Summary" in result["report"]


@pytest.mark.asyncio
async def test_generate_report_finds_conflicts(report_tools, sample_marketplace):
    """Test that report finds command conflicts"""
    result = await report_tools.generate_compatibility_report(
        sample_marketplace, "json"
    )

    assert "error" not in result
    assert result["summary"]["errors"] > 0
    assert result["summary"]["total_issues"] > 0


@pytest.mark.asyncio
async def test_generate_report_counts_correctly(report_tools, sample_marketplace):
    """Test summary counts are correct"""
    result = await report_tools.generate_compatibility_report(
        sample_marketplace, "json"
    )

    summary = result["summary"]
    assert summary["total_plugins"] == 3
    assert summary["total_commands"] == 3  # 3 commands total
    assert summary["total_tools"] == 5  # a, b, c, d, e


@pytest.mark.asyncio
async def test_generate_report_no_plugins(report_tools, marketplace_no_plugins):
    """Test error when no plugins found"""
    result = await report_tools.generate_compatibility_report(
        marketplace_no_plugins, "json"
    )

    assert "error" in result
    assert "no plugins" in result["error"].lower()


@pytest.mark.asyncio
async def test_generate_report_no_plugins_dir(report_tools, marketplace_no_dir):
    """Test error when plugins directory doesn't exist"""
    result = await report_tools.generate_compatibility_report(
        marketplace_no_dir, "json"
    )

    assert "error" in result
    assert "not found" in result["error"].lower()


@pytest.mark.asyncio
async def test_list_issues_all(report_tools, sample_marketplace):
    """Test listing all issues"""
    result = await report_tools.list_issues(sample_marketplace, "all", "all")

    assert "error" not in result
    assert "issues" in result
    assert result["total_issues"] > 0


@pytest.mark.asyncio
async def test_list_issues_filter_by_severity(report_tools, sample_marketplace):
    """Test filtering issues by severity"""
    all_result = await report_tools.list_issues(sample_marketplace, "all", "all")
    error_result = await report_tools.list_issues(sample_marketplace, "error", "all")

    # Error count should be less than or equal to all
    assert error_result["total_issues"] <= all_result["total_issues"]

    # All issues should have error severity
    for issue in error_result["issues"]:
        sev = issue.get("severity", "")
        if hasattr(sev, 'value'):
            sev = sev.value
        assert "error" in str(sev).lower()


@pytest.mark.asyncio
async def test_list_issues_filter_by_type(report_tools, sample_marketplace):
    """Test filtering issues by type"""
    result = await report_tools.list_issues(
        sample_marketplace, "all", "interface_mismatch"
    )

    # All issues should have matching type
    for issue in result["issues"]:
        itype = issue.get("issue_type", "")
        if hasattr(itype, 'value'):
            itype = itype.value
        assert "interface_mismatch" in str(itype).lower()


@pytest.mark.asyncio
async def test_list_issues_combined_filters(report_tools, sample_marketplace):
    """Test combined severity and type filters"""
    result = await report_tools.list_issues(
        sample_marketplace, "error", "interface_mismatch"
    )

    assert "error" not in result
    # Should have command conflict errors
    assert result["total_issues"] > 0


@pytest.mark.asyncio
async def test_report_markdown_has_all_sections(report_tools, sample_marketplace):
    """Test markdown report contains all expected sections"""
    result = await report_tools.generate_compatibility_report(
        sample_marketplace, "markdown"
    )

    report = result["report"]
    assert "## Summary" in report
    assert "## Plugins" in report
    # Compatibility section only if there are checks
    assert "Plugin One" in report or "plugin-one" in report.lower()


@pytest.mark.asyncio
async def test_report_includes_suggestions(report_tools, sample_marketplace):
    """Test that issues include suggestions"""
    result = await report_tools.generate_compatibility_report(
        sample_marketplace, "json"
    )

    issues = result.get("all_issues", [])
    # Find an issue with a suggestion
    issues_with_suggestions = [
        i for i in issues
        if i.get("suggestion")
    ]
    assert len(issues_with_suggestions) > 0
