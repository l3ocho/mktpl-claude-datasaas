"""
Parse tools for extracting interfaces from plugin documentation.

Provides structured extraction of:
- Plugin interfaces from README.md (commands, agents, tools)
- Agent definitions from CLAUDE.md (tool sequences, workflows)
"""
import re
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel


class ToolInfo(BaseModel):
    """Information about a single tool"""
    name: str
    category: Optional[str] = None
    description: Optional[str] = None


class CommandInfo(BaseModel):
    """Information about a plugin command"""
    name: str
    description: Optional[str] = None


class AgentInfo(BaseModel):
    """Information about a plugin agent"""
    name: str
    description: Optional[str] = None
    tools: list[str] = []


class PluginInterface(BaseModel):
    """Structured plugin interface extracted from README"""
    plugin_name: str
    description: Optional[str] = None
    commands: list[CommandInfo] = []
    agents: list[AgentInfo] = []
    tools: list[ToolInfo] = []
    tool_categories: dict[str, list[str]] = {}
    features: list[str] = []


class ClaudeMdAgent(BaseModel):
    """Agent definition extracted from CLAUDE.md"""
    name: str
    personality: Optional[str] = None
    responsibilities: list[str] = []
    tool_refs: list[str] = []
    workflow_steps: list[str] = []


class ParseTools:
    """Tools for parsing plugin documentation"""

    async def parse_plugin_interface(self, plugin_path: str) -> dict:
        """
        Parse plugin README.md to extract interface declarations.

        Args:
            plugin_path: Path to plugin directory or README.md file

        Returns:
            Structured interface with commands, agents, tools, etc.
        """
        # Resolve path to README
        path = Path(plugin_path)
        if path.is_dir():
            readme_path = path / "README.md"
        else:
            readme_path = path

        if not readme_path.exists():
            return {
                "error": f"README.md not found at {readme_path}",
                "plugin_path": plugin_path
            }

        content = readme_path.read_text()
        plugin_name = self._extract_plugin_name(content, path)

        interface = PluginInterface(
            plugin_name=plugin_name,
            description=self._extract_description(content),
            commands=self._extract_commands(content),
            agents=self._extract_agents_from_readme(content),
            tools=self._extract_tools(content),
            tool_categories=self._extract_tool_categories(content),
            features=self._extract_features(content)
        )

        return interface.model_dump()

    async def parse_claude_md_agents(self, claude_md_path: str) -> dict:
        """
        Parse CLAUDE.md to extract agent definitions and tool sequences.

        Args:
            claude_md_path: Path to CLAUDE.md file

        Returns:
            List of agents with their tool sequences
        """
        path = Path(claude_md_path)

        if not path.exists():
            return {
                "error": f"CLAUDE.md not found at {path}",
                "claude_md_path": claude_md_path
            }

        content = path.read_text()
        agents = self._extract_agents_from_claude_md(content)

        return {
            "file": str(path),
            "agents": [a.model_dump() for a in agents],
            "agent_count": len(agents)
        }

    def _extract_plugin_name(self, content: str, path: Path) -> str:
        """Extract plugin name from content or path"""
        # Try to get from H1 header
        match = re.search(r'^#\s+(.+?)(?:\s+Plugin|\s*$)', content, re.MULTILINE)
        if match:
            name = match.group(1).strip()
            # Handle cases like "# data-platform Plugin"
            name = re.sub(r'\s*Plugin\s*$', '', name, flags=re.IGNORECASE)
            return name

        # Fall back to directory name
        if path.is_dir():
            return path.name
        return path.parent.name

    def _extract_description(self, content: str) -> Optional[str]:
        """Extract plugin description from first paragraph after title"""
        # Get content after H1, before first H2
        match = re.search(r'^#\s+.+?\n\n(.+?)(?=\n##|\n\n##|\Z)', content, re.MULTILINE | re.DOTALL)
        if match:
            desc = match.group(1).strip()
            # Take first paragraph only
            desc = desc.split('\n\n')[0].strip()
            return desc
        return None

    def _extract_commands(self, content: str) -> list[CommandInfo]:
        """Extract commands from Commands section"""
        commands = []

        # Find Commands section
        commands_section = self._extract_section(content, "Commands")
        if not commands_section:
            return commands

        # Parse table format: | Command | Description |
        # Only match actual command names (start with / or alphanumeric)
        table_pattern = r'\|\s*`?(/[a-z][-a-z0-9]*)`?\s*\|\s*([^|]+)\s*\|'
        for match in re.finditer(table_pattern, commands_section):
            cmd_name = match.group(1).strip()
            desc = match.group(2).strip()

            # Skip header row and separators
            if cmd_name.lower() in ('command', 'commands') or cmd_name.startswith('-'):
                continue

            commands.append(CommandInfo(
                name=cmd_name,
                description=desc
            ))

        # Also look for ### `/command-name` format (with backticks)
        cmd_header_pattern = r'^###\s+`(/[a-z][-a-z0-9]*)`\s*\n(.+?)(?=\n###|\n##|\Z)'
        for match in re.finditer(cmd_header_pattern, commands_section, re.MULTILINE | re.DOTALL):
            cmd_name = match.group(1).strip()
            desc_block = match.group(2).strip()
            # Get first line or paragraph as description
            desc = desc_block.split('\n')[0].strip()

            # Don't duplicate if already found in table
            if not any(c.name == cmd_name for c in commands):
                commands.append(CommandInfo(name=cmd_name, description=desc))

        # Also look for ### /command-name format (without backticks)
        cmd_header_pattern2 = r'^###\s+(/[a-z][-a-z0-9]*)\s*\n(.+?)(?=\n###|\n##|\Z)'
        for match in re.finditer(cmd_header_pattern2, commands_section, re.MULTILINE | re.DOTALL):
            cmd_name = match.group(1).strip()
            desc_block = match.group(2).strip()
            # Get first line or paragraph as description
            desc = desc_block.split('\n')[0].strip()

            # Don't duplicate if already found in table
            if not any(c.name == cmd_name for c in commands):
                commands.append(CommandInfo(name=cmd_name, description=desc))

        return commands

    def _extract_agents_from_readme(self, content: str) -> list[AgentInfo]:
        """Extract agents from Agents section in README"""
        agents = []

        # Find Agents section
        agents_section = self._extract_section(content, "Agents")
        if not agents_section:
            return agents

        # Parse table format: | Agent | Description |
        # Only match actual agent names (alphanumeric with dashes/underscores)
        table_pattern = r'\|\s*`?([a-z][-a-z0-9_]*)`?\s*\|\s*([^|]+)\s*\|'
        for match in re.finditer(table_pattern, agents_section):
            agent_name = match.group(1).strip()
            desc = match.group(2).strip()

            # Skip header row and separators
            if agent_name.lower() in ('agent', 'agents') or agent_name.startswith('-'):
                continue

            agents.append(AgentInfo(name=agent_name, description=desc))

        return agents

    def _extract_tools(self, content: str) -> list[ToolInfo]:
        """Extract tool list from Tools Summary or similar section"""
        tools = []

        # Find Tools Summary section
        tools_section = self._extract_section(content, "Tools Summary")
        if not tools_section:
            tools_section = self._extract_section(content, "Tools")
        if not tools_section:
            tools_section = self._extract_section(content, "MCP Server Tools")

        if not tools_section:
            return tools

        # Parse category headers: ### category (N tools)
        category_pattern = r'###\s*(.+?)\s*(?:\((\d+)\s*tools?\))?\s*\n([^#]+)'
        for match in re.finditer(category_pattern, tools_section):
            category = match.group(1).strip()
            tool_list_text = match.group(3).strip()

            # Extract tool names from backtick lists
            tool_names = re.findall(r'`([a-z_]+)`', tool_list_text)
            for name in tool_names:
                tools.append(ToolInfo(name=name, category=category))

        # Also look for inline tool lists without categories
        inline_pattern = r'`([a-z_]+)`'
        all_tool_names = set(t.name for t in tools)
        for match in re.finditer(inline_pattern, tools_section):
            name = match.group(1)
            if name not in all_tool_names:
                tools.append(ToolInfo(name=name))
                all_tool_names.add(name)

        return tools

    def _extract_tool_categories(self, content: str) -> dict[str, list[str]]:
        """Extract tool categories with their tool lists"""
        categories = {}

        tools_section = self._extract_section(content, "Tools Summary")
        if not tools_section:
            tools_section = self._extract_section(content, "Tools")
        if not tools_section:
            return categories

        # Parse category headers: ### category (N tools)
        category_pattern = r'###\s*(.+?)\s*(?:\((\d+)\s*tools?\))?\s*\n([^#]+)'
        for match in re.finditer(category_pattern, tools_section):
            category = match.group(1).strip()
            tool_list_text = match.group(3).strip()

            # Extract tool names from backtick lists
            tool_names = re.findall(r'`([a-z_]+)`', tool_list_text)
            if tool_names:
                categories[category] = tool_names

        return categories

    def _extract_features(self, content: str) -> list[str]:
        """Extract features from Features section"""
        features = []

        features_section = self._extract_section(content, "Features")
        if not features_section:
            return features

        # Parse bullet points
        bullet_pattern = r'^[-*]\s+\*\*(.+?)\*\*'
        for match in re.finditer(bullet_pattern, features_section, re.MULTILINE):
            features.append(match.group(1).strip())

        return features

    def _extract_section(self, content: str, section_name: str) -> Optional[str]:
        """Extract content of a markdown section by header name"""
        # Match ## Section Name - include all content until next ## (same level or higher)
        pattern = rf'^##\s+{re.escape(section_name)}(?:\s*\([^)]*\))?\s*\n(.*?)(?=\n##[^#]|\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Try ### level - include content until next ## or ###
        pattern = rf'^###\s+{re.escape(section_name)}(?:\s*\([^)]*\))?\s*\n(.*?)(?=\n##|\n###[^#]|\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return None

    def _extract_agents_from_claude_md(self, content: str) -> list[ClaudeMdAgent]:
        """Extract agent definitions from CLAUDE.md"""
        agents = []

        # Look for Four-Agent Model section specifically
        # Match section headers like "### Four-Agent Model (projman)" or "## Four-Agent Model"
        agent_model_match = re.search(
            r'^##[#]?\s+Four-Agent Model.*?\n(.*?)(?=\n##[^#]|\Z)',
            content, re.MULTILINE | re.DOTALL
        )
        agent_model_section = agent_model_match.group(1) if agent_model_match else None

        if agent_model_section:
            # Parse agent table within this section
            # | **Planner** | Thoughtful, methodical | Sprint planning, ... |
            # Match rows where first cell starts with ** (bold) and contains a capitalized word
            agent_table_pattern = r'\|\s*\*\*([A-Z][a-zA-Z\s]+?)\*\*\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'

            for match in re.finditer(agent_table_pattern, agent_model_section):
                agent_name = match.group(1).strip()
                personality = match.group(2).strip()
                responsibilities = match.group(3).strip()

                # Skip header rows and separator rows
                if agent_name.lower() in ('agent', 'agents', '---', '-', ''):
                    continue
                if 'personality' in personality.lower() or '---' in personality:
                    continue

                # Skip if personality looks like tool names (contains backticks)
                if '`' in personality:
                    continue

                # Extract tool references from responsibilities
                tool_refs = re.findall(r'`([a-z_]+)`', responsibilities)

                # Split responsibilities by comma
                resp_list = [r.strip() for r in responsibilities.split(',')]

                agents.append(ClaudeMdAgent(
                    name=agent_name,
                    personality=personality,
                    responsibilities=resp_list,
                    tool_refs=tool_refs
                ))

        # Also look for agents table in ## Agents section
        agents_section = self._extract_section(content, "Agents")
        if agents_section:
            # Parse table: | Agent | Description |
            table_pattern = r'\|\s*`?([a-z][-a-z0-9_]+)`?\s*\|\s*([^|]+)\s*\|'
            for match in re.finditer(table_pattern, agents_section):
                agent_name = match.group(1).strip()
                desc = match.group(2).strip()

                # Skip header rows
                if agent_name.lower() in ('agent', 'agents', '---', '-'):
                    continue

                # Check if agent already exists
                if not any(a.name.lower() == agent_name.lower() for a in agents):
                    agents.append(ClaudeMdAgent(
                        name=agent_name,
                        responsibilities=[desc] if desc else []
                    ))

        # Look for workflow sections to enrich agent data
        workflow_section = self._extract_section(content, "Workflow")
        if workflow_section:
            # Parse numbered steps
            step_pattern = r'^\d+\.\s+(.+?)$'
            workflow_steps = re.findall(step_pattern, workflow_section, re.MULTILINE)

            # Associate workflow steps with agents mentioned
            for agent in agents:
                for step in workflow_steps:
                    if agent.name.lower() in step.lower():
                        agent.workflow_steps.append(step)
                        # Extract any tool references in the step
                        step_tools = re.findall(r'`([a-z_]+)`', step)
                        agent.tool_refs.extend(t for t in step_tools if t not in agent.tool_refs)

        # Look for agent-specific sections (### Planner Agent)
        agent_section_pattern = r'^###?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+Agent\s*\n(.*?)(?=\n##|\n###|\Z)'
        for match in re.finditer(agent_section_pattern, content, re.MULTILINE | re.DOTALL):
            agent_name = match.group(1).strip()
            section_content = match.group(2).strip()

            # Check if agent already exists
            existing = next((a for a in agents if a.name.lower() == agent_name.lower()), None)
            if existing:
                # Add tool refs from this section
                tool_refs = re.findall(r'`([a-z_]+)`', section_content)
                existing.tool_refs.extend(t for t in tool_refs if t not in existing.tool_refs)
            else:
                tool_refs = re.findall(r'`([a-z_]+)`', section_content)
                agents.append(ClaudeMdAgent(
                    name=agent_name,
                    tool_refs=tool_refs
                ))

        return agents
