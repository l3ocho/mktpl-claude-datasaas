"""
Validation tools for checking cross-plugin compatibility and agent references.

Provides:
- validate_compatibility: Compare two plugin interfaces
- validate_agent_refs: Check agent tool references exist
- validate_data_flow: Verify data flow through agent sequences
"""
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from enum import Enum

from .parse_tools import ParseTools, PluginInterface, ClaudeMdAgent


class IssueSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class IssueType(str, Enum):
    MISSING_TOOL = "missing_tool"
    INTERFACE_MISMATCH = "interface_mismatch"
    OPTIONAL_DEPENDENCY = "optional_dependency"
    UNDECLARED_OUTPUT = "undeclared_output"
    INVALID_SEQUENCE = "invalid_sequence"


class ValidationIssue(BaseModel):
    """A single validation issue"""
    severity: IssueSeverity
    issue_type: IssueType
    message: str
    location: Optional[str] = None
    suggestion: Optional[str] = None


class CompatibilityResult(BaseModel):
    """Result of compatibility check between two plugins"""
    plugin_a: str
    plugin_b: str
    compatible: bool
    shared_tools: list[str] = []
    a_only_tools: list[str] = []
    b_only_tools: list[str] = []
    issues: list[ValidationIssue] = []


class AgentValidationResult(BaseModel):
    """Result of agent reference validation"""
    agent_name: str
    valid: bool
    tool_refs_found: list[str] = []
    tool_refs_missing: list[str] = []
    issues: list[ValidationIssue] = []


class DataFlowResult(BaseModel):
    """Result of data flow validation"""
    agent_name: str
    valid: bool
    flow_steps: list[str] = []
    issues: list[ValidationIssue] = []


class ValidationTools:
    """Tools for validating plugin compatibility and agent references"""

    def __init__(self):
        self.parse_tools = ParseTools()

    async def validate_compatibility(self, plugin_a: str, plugin_b: str) -> dict:
        """
        Validate compatibility between two plugin interfaces.

        Compares tools, commands, and agents to identify overlaps and gaps.

        Args:
            plugin_a: Path to first plugin directory
            plugin_b: Path to second plugin directory

        Returns:
            Compatibility report with shared tools, unique tools, and issues
        """
        # Parse both plugins
        interface_a = await self.parse_tools.parse_plugin_interface(plugin_a)
        interface_b = await self.parse_tools.parse_plugin_interface(plugin_b)

        # Check for parse errors
        if "error" in interface_a:
            return {
                "error": f"Failed to parse plugin A: {interface_a['error']}",
                "plugin_a": plugin_a,
                "plugin_b": plugin_b
            }
        if "error" in interface_b:
            return {
                "error": f"Failed to parse plugin B: {interface_b['error']}",
                "plugin_a": plugin_a,
                "plugin_b": plugin_b
            }

        # Extract tool names
        tools_a = set(t["name"] for t in interface_a.get("tools", []))
        tools_b = set(t["name"] for t in interface_b.get("tools", []))

        # Find overlaps and differences
        shared = tools_a & tools_b
        a_only = tools_a - tools_b
        b_only = tools_b - tools_a

        issues = []

        # Check for potential naming conflicts
        if shared:
            issues.append(ValidationIssue(
                severity=IssueSeverity.WARNING,
                issue_type=IssueType.INTERFACE_MISMATCH,
                message=f"Both plugins define tools with same names: {list(shared)}",
                location=f"{interface_a['plugin_name']} and {interface_b['plugin_name']}",
                suggestion="Ensure tools with same names have compatible interfaces"
            ))

        # Check command overlaps
        cmds_a = set(c["name"] for c in interface_a.get("commands", []))
        cmds_b = set(c["name"] for c in interface_b.get("commands", []))
        shared_cmds = cmds_a & cmds_b

        if shared_cmds:
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                issue_type=IssueType.INTERFACE_MISMATCH,
                message=f"Command name conflict: {list(shared_cmds)}",
                location=f"{interface_a['plugin_name']} and {interface_b['plugin_name']}",
                suggestion="Rename conflicting commands to avoid ambiguity"
            ))

        result = CompatibilityResult(
            plugin_a=interface_a["plugin_name"],
            plugin_b=interface_b["plugin_name"],
            compatible=len([i for i in issues if i.severity == IssueSeverity.ERROR]) == 0,
            shared_tools=list(shared),
            a_only_tools=list(a_only),
            b_only_tools=list(b_only),
            issues=issues
        )

        return result.model_dump()

    async def validate_agent_refs(
        self,
        agent_name: str,
        claude_md_path: str,
        plugin_paths: list[str] = None
    ) -> dict:
        """
        Validate that all tool references in an agent definition exist.

        Args:
            agent_name: Name of the agent to validate
            claude_md_path: Path to CLAUDE.md containing the agent
            plugin_paths: Optional list of plugin paths to check for tools

        Returns:
            Validation result with found/missing tools and issues
        """
        # Parse CLAUDE.md for agents
        agents_result = await self.parse_tools.parse_claude_md_agents(claude_md_path)

        if "error" in agents_result:
            return {
                "error": agents_result["error"],
                "agent_name": agent_name
            }

        # Find the specific agent
        agent = None
        for a in agents_result.get("agents", []):
            if a["name"].lower() == agent_name.lower():
                agent = a
                break

        if not agent:
            return {
                "error": f"Agent '{agent_name}' not found in {claude_md_path}",
                "agent_name": agent_name,
                "available_agents": [a["name"] for a in agents_result.get("agents", [])]
            }

        # Collect all available tools from plugins
        available_tools = set()
        if plugin_paths:
            for plugin_path in plugin_paths:
                interface = await self.parse_tools.parse_plugin_interface(plugin_path)
                if "error" not in interface:
                    for tool in interface.get("tools", []):
                        available_tools.add(tool["name"])

        # Check agent tool references
        tool_refs = set(agent.get("tool_refs", []))
        found = tool_refs & available_tools if available_tools else tool_refs
        missing = tool_refs - available_tools if available_tools else set()

        issues = []

        # Report missing tools
        for tool in missing:
            issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                issue_type=IssueType.MISSING_TOOL,
                message=f"Agent '{agent_name}' references tool '{tool}' which is not found",
                location=claude_md_path,
                suggestion=f"Check if tool '{tool}' exists or fix the reference"
            ))

        # Check if agent has no tool refs (might be incomplete)
        if not tool_refs:
            issues.append(ValidationIssue(
                severity=IssueSeverity.INFO,
                issue_type=IssueType.UNDECLARED_OUTPUT,
                message=f"Agent '{agent_name}' has no documented tool references",
                location=claude_md_path,
                suggestion="Consider documenting which tools this agent uses"
            ))

        result = AgentValidationResult(
            agent_name=agent_name,
            valid=len([i for i in issues if i.severity == IssueSeverity.ERROR]) == 0,
            tool_refs_found=list(found),
            tool_refs_missing=list(missing),
            issues=issues
        )

        return result.model_dump()

    async def validate_data_flow(self, agent_name: str, claude_md_path: str) -> dict:
        """
        Validate data flow through an agent's tool sequence.

        Checks that each step's expected output can be used by the next step.

        Args:
            agent_name: Name of the agent to validate
            claude_md_path: Path to CLAUDE.md containing the agent

        Returns:
            Data flow validation result with steps and issues
        """
        # Parse CLAUDE.md for agents
        agents_result = await self.parse_tools.parse_claude_md_agents(claude_md_path)

        if "error" in agents_result:
            return {
                "error": agents_result["error"],
                "agent_name": agent_name
            }

        # Find the specific agent
        agent = None
        for a in agents_result.get("agents", []):
            if a["name"].lower() == agent_name.lower():
                agent = a
                break

        if not agent:
            return {
                "error": f"Agent '{agent_name}' not found in {claude_md_path}",
                "agent_name": agent_name,
                "available_agents": [a["name"] for a in agents_result.get("agents", [])]
            }

        issues = []
        flow_steps = []

        # Extract workflow steps
        workflow_steps = agent.get("workflow_steps", [])
        responsibilities = agent.get("responsibilities", [])

        # Build flow from workflow steps or responsibilities
        steps = workflow_steps if workflow_steps else responsibilities

        for i, step in enumerate(steps):
            flow_steps.append(f"Step {i+1}: {step}")

        # Check for data flow patterns
        tool_refs = agent.get("tool_refs", [])

        # Known data flow patterns
        # e.g., data-platform produces data_ref, viz-platform consumes it
        known_producers = {
            "read_csv": "data_ref",
            "read_parquet": "data_ref",
            "pg_query": "data_ref",
            "filter": "data_ref",
            "groupby": "data_ref",
        }

        known_consumers = {
            "describe": "data_ref",
            "head": "data_ref",
            "tail": "data_ref",
            "to_csv": "data_ref",
            "to_parquet": "data_ref",
        }

        # Check if agent uses tools that require data_ref
        has_producer = any(t in known_producers for t in tool_refs)
        has_consumer = any(t in known_consumers for t in tool_refs)

        if has_consumer and not has_producer:
            issues.append(ValidationIssue(
                severity=IssueSeverity.WARNING,
                issue_type=IssueType.INTERFACE_MISMATCH,
                message=f"Agent '{agent_name}' uses tools that consume data_ref but no producer found",
                location=claude_md_path,
                suggestion="Ensure a data loading tool (read_csv, pg_query, etc.) is used before data consumers"
            ))

        # Check for empty workflow
        if not steps and not tool_refs:
            issues.append(ValidationIssue(
                severity=IssueSeverity.INFO,
                issue_type=IssueType.UNDECLARED_OUTPUT,
                message=f"Agent '{agent_name}' has no documented workflow or tool sequence",
                location=claude_md_path,
                suggestion="Consider documenting the agent's workflow steps"
            ))

        result = DataFlowResult(
            agent_name=agent_name,
            valid=len([i for i in issues if i.severity == IssueSeverity.ERROR]) == 0,
            flow_steps=flow_steps,
            issues=issues
        )

        return result.model_dump()
