"""
Report tools for generating compatibility reports and listing issues.

Provides:
- generate_compatibility_report: Full marketplace validation report
- list_issues: Filtered issue listing
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .parse_tools import ParseTools
from .validation_tools import ValidationTools, IssueSeverity, IssueType, ValidationIssue


class ReportSummary(BaseModel):
    """Summary statistics for a report"""
    total_plugins: int = 0
    total_commands: int = 0
    total_agents: int = 0
    total_tools: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0


class ReportTools:
    """Tools for generating reports and listing issues"""

    def __init__(self):
        self.parse_tools = ParseTools()
        self.validation_tools = ValidationTools()

    async def generate_compatibility_report(
        self,
        marketplace_path: str,
        format: str = "markdown"
    ) -> dict:
        """
        Generate a comprehensive compatibility report for all plugins.

        Args:
            marketplace_path: Path to marketplace root directory
            format: Output format ("markdown" or "json")

        Returns:
            Full compatibility report with all findings
        """
        marketplace = Path(marketplace_path)
        plugins_dir = marketplace / "plugins"

        if not plugins_dir.exists():
            return {
                "error": f"Plugins directory not found at {plugins_dir}",
                "marketplace_path": marketplace_path
            }

        # Discover all plugins
        plugins = []
        for item in plugins_dir.iterdir():
            if item.is_dir() and (item / ".claude-plugin").exists():
                plugins.append(item)

        if not plugins:
            return {
                "error": "No plugins found in marketplace",
                "marketplace_path": marketplace_path
            }

        # Parse all plugin interfaces
        interfaces = {}
        all_issues = []
        summary = ReportSummary(total_plugins=len(plugins))

        for plugin_path in plugins:
            interface = await self.parse_tools.parse_plugin_interface(str(plugin_path))
            if "error" not in interface:
                interfaces[interface["plugin_name"]] = interface
                summary.total_commands += len(interface.get("commands", []))
                summary.total_agents += len(interface.get("agents", []))
                summary.total_tools += len(interface.get("tools", []))

        # Run pairwise compatibility checks
        plugin_names = list(interfaces.keys())
        compatibility_results = []

        for i, name_a in enumerate(plugin_names):
            for name_b in plugin_names[i+1:]:
                path_a = plugins_dir / self._find_plugin_dir(plugins_dir, name_a)
                path_b = plugins_dir / self._find_plugin_dir(plugins_dir, name_b)

                result = await self.validation_tools.validate_compatibility(
                    str(path_a), str(path_b)
                )

                if "error" not in result:
                    compatibility_results.append(result)
                    all_issues.extend(result.get("issues", []))

        # Parse CLAUDE.md if exists
        claude_md = marketplace / "CLAUDE.md"
        agents_from_claude = []
        if claude_md.exists():
            agents_result = await self.parse_tools.parse_claude_md_agents(str(claude_md))
            if "error" not in agents_result:
                agents_from_claude = agents_result.get("agents", [])

                # Validate each agent
                for agent in agents_from_claude:
                    agent_result = await self.validation_tools.validate_agent_refs(
                        agent["name"],
                        str(claude_md),
                        [str(p) for p in plugins]
                    )
                    if "error" not in agent_result:
                        all_issues.extend(agent_result.get("issues", []))

        # Count issues by severity
        for issue in all_issues:
            severity = issue.get("severity", "info")
            if isinstance(severity, str):
                severity_str = severity.lower()
            else:
                severity_str = severity.value if hasattr(severity, 'value') else str(severity).lower()

            if "error" in severity_str:
                summary.errors += 1
            elif "warning" in severity_str:
                summary.warnings += 1
            else:
                summary.info += 1

        summary.total_issues = len(all_issues)

        # Generate report
        if format == "json":
            return {
                "generated_at": datetime.now().isoformat(),
                "marketplace_path": marketplace_path,
                "summary": summary.model_dump(),
                "plugins": interfaces,
                "compatibility_checks": compatibility_results,
                "claude_md_agents": agents_from_claude,
                "all_issues": all_issues
            }
        else:
            # Generate markdown report
            report = self._generate_markdown_report(
                marketplace_path,
                summary,
                interfaces,
                compatibility_results,
                agents_from_claude,
                all_issues
            )
            return {
                "generated_at": datetime.now().isoformat(),
                "marketplace_path": marketplace_path,
                "summary": summary.model_dump(),
                "report": report
            }

    def _find_plugin_dir(self, plugins_dir: Path, plugin_name: str) -> str:
        """Find plugin directory by name (handles naming variations)"""
        # Try exact match first
        for item in plugins_dir.iterdir():
            if item.is_dir():
                if item.name.lower() == plugin_name.lower():
                    return item.name
                # Check plugin.json for name
                plugin_json = item / ".claude-plugin" / "plugin.json"
                if plugin_json.exists():
                    import json
                    try:
                        data = json.loads(plugin_json.read_text())
                        if data.get("name", "").lower() == plugin_name.lower():
                            return item.name
                    except:
                        pass
        return plugin_name

    def _generate_markdown_report(
        self,
        marketplace_path: str,
        summary: ReportSummary,
        interfaces: dict,
        compatibility_results: list,
        agents: list,
        issues: list
    ) -> str:
        """Generate markdown formatted report"""
        lines = [
            "# Contract Validation Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Marketplace:** `{marketplace_path}`",
            "",
            "## Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Plugins | {summary.total_plugins} |",
            f"| Commands | {summary.total_commands} |",
            f"| Agents | {summary.total_agents} |",
            f"| Tools | {summary.total_tools} |",
            f"| **Issues** | **{summary.total_issues}** |",
            f"| - Errors | {summary.errors} |",
            f"| - Warnings | {summary.warnings} |",
            f"| - Info | {summary.info} |",
            "",
        ]

        # Plugin details
        lines.extend([
            "## Plugins",
            "",
        ])

        for name, interface in interfaces.items():
            cmds = len(interface.get("commands", []))
            agents_count = len(interface.get("agents", []))
            tools = len(interface.get("tools", []))
            lines.append(f"### {name}")
            lines.append("")
            lines.append(f"- Commands: {cmds}")
            lines.append(f"- Agents: {agents_count}")
            lines.append(f"- Tools: {tools}")
            lines.append("")

        # Compatibility results
        if compatibility_results:
            lines.extend([
                "## Compatibility Checks",
                "",
            ])

            for result in compatibility_results:
                status = "✓" if result.get("compatible", True) else "✗"
                lines.append(f"### {result['plugin_a']} ↔ {result['plugin_b']} {status}")
                lines.append("")

                if result.get("shared_tools"):
                    lines.append(f"- Shared tools: `{', '.join(result['shared_tools'])}`")
                if result.get("issues"):
                    for issue in result["issues"]:
                        sev = issue.get("severity", "info")
                        if hasattr(sev, 'value'):
                            sev = sev.value
                        lines.append(f"- [{sev.upper()}] {issue['message']}")
                lines.append("")

        # Issues section
        if issues:
            lines.extend([
                "## All Issues",
                "",
                "| Severity | Type | Message |",
                "|----------|------|---------|",
            ])

            for issue in issues:
                sev = issue.get("severity", "info")
                itype = issue.get("issue_type", "unknown")
                msg = issue.get("message", "")

                if hasattr(sev, 'value'):
                    sev = sev.value
                if hasattr(itype, 'value'):
                    itype = itype.value

                # Truncate message for table
                msg_short = msg[:60] + "..." if len(msg) > 60 else msg
                lines.append(f"| {sev} | {itype} | {msg_short} |")

            lines.append("")

        return "\n".join(lines)

    async def list_issues(
        self,
        marketplace_path: str,
        severity: str = "all",
        issue_type: str = "all"
    ) -> dict:
        """
        List validation issues with optional filtering.

        Args:
            marketplace_path: Path to marketplace root directory
            severity: Filter by severity ("error", "warning", "info", "all")
            issue_type: Filter by type ("missing_tool", "interface_mismatch", etc., "all")

        Returns:
            Filtered list of issues
        """
        # Generate full report first
        report = await self.generate_compatibility_report(marketplace_path, format="json")

        if "error" in report:
            return report

        all_issues = report.get("all_issues", [])

        # Filter by severity
        if severity != "all":
            filtered = []
            for issue in all_issues:
                issue_sev = issue.get("severity", "info")
                if hasattr(issue_sev, 'value'):
                    issue_sev = issue_sev.value
                if isinstance(issue_sev, str) and severity.lower() in issue_sev.lower():
                    filtered.append(issue)
            all_issues = filtered

        # Filter by type
        if issue_type != "all":
            filtered = []
            for issue in all_issues:
                itype = issue.get("issue_type", "unknown")
                if hasattr(itype, 'value'):
                    itype = itype.value
                if isinstance(itype, str) and issue_type.lower() in itype.lower():
                    filtered.append(issue)
            all_issues = filtered

        return {
            "marketplace_path": marketplace_path,
            "filters": {
                "severity": severity,
                "issue_type": issue_type
            },
            "total_issues": len(all_issues),
            "issues": all_issues
        }
