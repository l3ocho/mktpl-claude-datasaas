"""
Tool registry for Gitea MCP Server.

Provides transport-agnostic tool definitions and dispatch logic that can be
used by both the stdio server and external consumers (e.g., HTTP transport).

Usage:
    from mcp_server.tool_registry import get_tool_definitions, create_tool_dispatcher

    # Get all tool schemas
    tools = get_tool_definitions()

    # Get filtered tool schemas
    tools = get_tool_definitions(tool_filter=["list_issues", "get_issue"])

    # Create dispatcher
    dispatch = create_tool_dispatcher(client)
    result = await dispatch("list_issues", {"state": "open"})
"""
import json
import logging
from typing import Callable, Awaitable, Optional

from mcp.types import Tool, TextContent

from .gitea_client import GiteaClient
from .tools.issues import IssueTools
from .tools.labels import LabelTools
from .tools.wiki import WikiTools
from .tools.milestones import MilestoneTools
from .tools.dependencies import DependencyTools
from .tools.pull_requests import PullRequestTools

logger = logging.getLogger(__name__)


def _coerce_types(arguments: dict) -> dict:
    """
    Coerce argument types to handle MCP serialization quirks.

    MCP sometimes passes integers as strings and arrays as JSON strings.
    This function normalizes them to the expected Python types.
    """
    coerced = {}
    for key, value in arguments.items():
        if value is None:
            coerced[key] = value
            continue

        # Coerce integer fields
        int_fields = {'issue_number', 'milestone_id', 'pr_number', 'depends_on', 'milestone', 'limit'}
        if key in int_fields and isinstance(value, str):
            try:
                coerced[key] = int(value)
                continue
            except ValueError:
                pass

        # Coerce array fields that might be JSON strings
        array_fields = {'labels', 'tags', 'issue_numbers', 'comments'}
        if key in array_fields and isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    coerced[key] = parsed
                    continue
            except json.JSONDecodeError:
                pass

        coerced[key] = value

    return coerced


def _get_all_tool_definitions() -> list[Tool]:
    """
    Return the complete list of Tool definitions.

    This is the single source of truth for all tool schemas.
    """
    return [
        Tool(
            name="list_issues",
            description="List issues from Gitea repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open",
                        "description": "Issue state filter"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by labels"
                    },
                    "milestone": {
                        "type": "string",
                        "description": "Filter by milestone title (exact match)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (for PMO mode)"
                    }
                }
            }
        ),
        Tool(
            name="get_issue",
            description="Get specific issue details",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": ["integer", "string"],
                        "description": "Issue number"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (for PMO mode)"
                    }
                },
                "required": ["issue_number"]
            }
        ),
        Tool(
            name="create_issue",
            description="Create a new issue in Gitea",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Issue title"
                    },
                    "body": {
                        "type": "string",
                        "description": "Issue description"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of label names"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (for PMO mode)"
                    }
                },
                "required": ["title", "body"]
            }
        ),
        Tool(
            name="update_issue",
            description="Update existing issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": ["integer", "string"],
                        "description": "Issue number"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title"
                    },
                    "body": {
                        "type": "string",
                        "description": "New body"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed"],
                        "description": "New state"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "New labels"
                    },
                    "milestone": {
                        "type": ["integer", "string"],
                        "description": "Milestone ID to assign"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (for PMO mode)"
                    }
                },
                "required": ["issue_number"]
            }
        ),
        Tool(
            name="add_comment",
            description="Add comment to issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": ["integer", "string"],
                        "description": "Issue number"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comment text"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (for PMO mode)"
                    }
                },
                "required": ["issue_number", "comment"]
            }
        ),
        Tool(
            name="get_labels",
            description="Get all available labels (org + repo)",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "Repository name (for PMO mode)"
                    }
                }
            }
        ),
        Tool(
            name="suggest_labels",
            description="Analyze context and suggest appropriate labels",
            inputSchema={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Issue title + description or sprint context"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["context"]
            }
        ),
        Tool(
            name="aggregate_issues",
            description="Fetch issues across all repositories (PMO mode)",
            inputSchema={
                "type": "object",
                "properties": {
                    "org": {
                        "type": "string",
                        "description": "Organization name (e.g. 'bandit')"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open",
                        "description": "Issue state filter"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by labels"
                    }
                },
                "required": ["org"]
            }
        ),
        # Wiki Tools (Lessons Learned)
        Tool(
            name="list_wiki_pages",
            description="List all wiki pages in repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                }
            }
        ),
        Tool(
            name="get_wiki_page",
            description="Get a specific wiki page by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_name": {
                        "type": "string",
                        "description": "Wiki page name/path"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["page_name"]
            }
        ),
        Tool(
            name="create_wiki_page",
            description="Create a new wiki page",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Page title/name"
                    },
                    "content": {
                        "type": "string",
                        "description": "Page content (markdown)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="update_wiki_page",
            description="Update an existing wiki page",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_name": {
                        "type": "string",
                        "description": "Wiki page name/path"
                    },
                    "content": {
                        "type": "string",
                        "description": "New page content (markdown)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["page_name", "content"]
            }
        ),
        Tool(
            name="create_lesson",
            description="Create a lessons learned entry in the wiki",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Lesson title (e.g., 'Sprint 16 - Prevent Infinite Loops')"
                    },
                    "content": {
                        "type": "string",
                        "description": "Lesson content (markdown with context, problem, solution, prevention)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization"
                    },
                    "category": {
                        "type": "string",
                        "default": "sprints",
                        "description": "Category (sprints, patterns, architecture, etc.)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["title", "content", "tags"]
            }
        ),
        Tool(
            name="search_lessons",
            description="Search lessons learned from previous sprints",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (optional)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags to filter by (optional)"
                    },
                    "limit": {
                        "type": ["integer", "string"],
                        "default": 20,
                        "description": "Maximum results"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                }
            }
        ),
        Tool(
            name="allocate_rfc_number",
            description="Allocate the next available RFC number by scanning existing RFC wiki pages",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                }
            }
        ),
        # Milestone Tools
        Tool(
            name="list_milestones",
            description="List all milestones in repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open",
                        "description": "Milestone state filter"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                }
            }
        ),
        Tool(
            name="get_milestone",
            description="Get a specific milestone by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "milestone_id": {
                        "type": ["integer", "string"],
                        "description": "Milestone ID"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["milestone_id"]
            }
        ),
        Tool(
            name="create_milestone",
            description="Create a new milestone",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Milestone title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Milestone description"
                    },
                    "due_on": {
                        "type": "string",
                        "description": "Due date (ISO 8601 format)"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="update_milestone",
            description="Update an existing milestone",
            inputSchema={
                "type": "object",
                "properties": {
                    "milestone_id": {
                        "type": ["integer", "string"],
                        "description": "Milestone ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed"],
                        "description": "New state"
                    },
                    "due_on": {
                        "type": "string",
                        "description": "New due date"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["milestone_id"]
            }
        ),
        Tool(
            name="delete_milestone",
            description="Delete a milestone",
            inputSchema={
                "type": "object",
                "properties": {
                    "milestone_id": {
                        "type": ["integer", "string"],
                        "description": "Milestone ID"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["milestone_id"]
            }
        ),
        # Dependency Tools
        Tool(
            name="list_issue_dependencies",
            description="List all dependencies for an issue (issues that block this one)",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": ["integer", "string"],
                        "description": "Issue number"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["issue_number"]
            }
        ),
        Tool(
            name="create_issue_dependency",
            description="Create a dependency (issue depends on another issue)",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": ["integer", "string"],
                        "description": "Issue that will depend on another"
                    },
                    "depends_on": {
                        "type": ["integer", "string"],
                        "description": "Issue that blocks issue_number"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["issue_number", "depends_on"]
            }
        ),
        Tool(
            name="remove_issue_dependency",
            description="Remove a dependency between issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": ["integer", "string"],
                        "description": "Issue that depends on another"
                    },
                    "depends_on": {
                        "type": ["integer", "string"],
                        "description": "Issue being depended on"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["issue_number", "depends_on"]
            }
        ),
        Tool(
            name="get_execution_order",
            description="Get parallelizable execution order for issues based on dependencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_numbers": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of issue numbers to analyze"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["issue_numbers"]
            }
        ),
        # Validation Tools
        Tool(
            name="validate_repo_org",
            description="Check if repository belongs to an organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                }
            }
        ),
        Tool(
            name="get_branch_protection",
            description="Get branch protection rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "branch": {
                        "type": "string",
                        "description": "Branch name"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["branch"]
            }
        ),
        Tool(
            name="create_label",
            description="Create a new label in the repository (for repo-specific labels like Component/*, Tech/*)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Label name (e.g., 'Component/Backend', 'Tech/Python')"
                    },
                    "color": {
                        "type": "string",
                        "description": "Label color (hex code)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Label description"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["name", "color"]
            }
        ),
        Tool(
            name="create_org_label",
            description="Create a new label at organization level (for workflow labels like Type/*, Priority/*, Complexity/*, Effort/*)",
            inputSchema={
                "type": "object",
                "properties": {
                    "org": {
                        "type": "string",
                        "description": "Organization name"
                    },
                    "name": {
                        "type": "string",
                        "description": "Label name (e.g., 'Type/Bug', 'Priority/High')"
                    },
                    "color": {
                        "type": "string",
                        "description": "Label color (hex code)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Label description"
                    }
                },
                "required": ["org", "name", "color"]
            }
        ),
        Tool(
            name="create_label_smart",
            description="Create a label at the appropriate level (org or repo) based on category. Org: Type/*, Priority/*, Complexity/*, Effort/*, Risk/*, Source/*, Agent/*. Repo: Component/*, Tech/*",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Label name (e.g., 'Type/Bug', 'Component/Backend')"
                    },
                    "color": {
                        "type": "string",
                        "description": "Label color (hex code)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Label description"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["name", "color"]
            }
        ),
        # Pull Request Tools
        Tool(
            name="list_pull_requests",
            description="List pull requests from repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open",
                        "description": "PR state filter"
                    },
                    "sort": {
                        "type": "string",
                        "enum": ["oldest", "recentupdate", "leastupdate", "mostcomment", "leastcomment", "priority"],
                        "default": "recentupdate",
                        "description": "Sort order"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by labels"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                }
            }
        ),
        Tool(
            name="get_pull_request",
            description="Get specific pull request details",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {
                        "type": ["integer", "string"],
                        "description": "Pull request number"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["pr_number"]
            }
        ),
        Tool(
            name="get_pr_diff",
            description="Get the diff for a pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {
                        "type": ["integer", "string"],
                        "description": "Pull request number"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["pr_number"]
            }
        ),
        Tool(
            name="get_pr_comments",
            description="Get comments on a pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {
                        "type": ["integer", "string"],
                        "description": "Pull request number"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["pr_number"]
            }
        ),
        Tool(
            name="create_pr_review",
            description="Create a review on a pull request (approve, request changes, or comment)",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {
                        "type": ["integer", "string"],
                        "description": "Pull request number"
                    },
                    "body": {
                        "type": "string",
                        "description": "Review body/summary"
                    },
                    "event": {
                        "type": "string",
                        "enum": ["APPROVE", "REQUEST_CHANGES", "COMMENT"],
                        "default": "COMMENT",
                        "description": "Review action"
                    },
                    "comments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "position": {"type": ["integer", "string"]},
                                "body": {"type": "string"}
                            }
                        },
                        "description": "Optional inline comments"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["pr_number", "body"]
            }
        ),
        Tool(
            name="add_pr_comment",
            description="Add a general comment to a pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {
                        "type": ["integer", "string"],
                        "description": "Pull request number"
                    },
                    "body": {
                        "type": "string",
                        "description": "Comment text"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["pr_number", "body"]
            }
        ),
        Tool(
            name="create_pull_request",
            description="Create a new pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "PR title"
                    },
                    "body": {
                        "type": "string",
                        "description": "PR description/body"
                    },
                    "head": {
                        "type": "string",
                        "description": "Source branch name (the branch with changes)"
                    },
                    "base": {
                        "type": "string",
                        "description": "Target branch name (the branch to merge into)"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of label names"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name (owner/repo format)"
                    }
                },
                "required": ["title", "body", "head", "base"]
            }
        )
    ]


def get_tool_definitions(tool_filter: Optional[list[str]] = None) -> list[Tool]:
    """
    Get tool definitions, optionally filtered by name.

    Args:
        tool_filter: Optional list of tool names to include. If None, returns all tools.

    Returns:
        List of Tool objects
    """
    all_tools = _get_all_tool_definitions()

    if tool_filter is None:
        return all_tools

    filter_set = set(tool_filter)
    return [tool for tool in all_tools if tool.name in filter_set]


def create_tool_dispatcher(
    client: GiteaClient,
    tool_filter: Optional[list[str]] = None
) -> Callable[[str, dict], Awaitable[list[TextContent]]]:
    """
    Create a tool dispatcher function bound to the given client.

    Args:
        client: GiteaClient instance
        tool_filter: Optional list of tool names to allow. If None, all tools are allowed.

    Returns:
        Async function that dispatches tool calls: dispatch(name, arguments) -> list[TextContent]
    """
    # Initialize tool handlers
    issue_tools = IssueTools(client)
    label_tools = LabelTools(client)
    wiki_tools = WikiTools(client)
    milestone_tools = MilestoneTools(client)
    dependency_tools = DependencyTools(client)
    pr_tools = PullRequestTools(client)

    # Build filter set if provided
    filter_set = set(tool_filter) if tool_filter else None

    async def dispatch(name: str, arguments: dict) -> list[TextContent]:
        """
        Dispatch a tool call to the appropriate handler.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            List of TextContent with results
        """
        try:
            # Check filter if provided
            if filter_set and name not in filter_set:
                raise ValueError(f"Tool not available: {name}")

            # Coerce types to handle MCP serialization quirks
            arguments = _coerce_types(arguments)

            # Route to appropriate tool handler
            if name == "list_issues":
                result = await issue_tools.list_issues(**arguments)
            elif name == "get_issue":
                result = await issue_tools.get_issue(**arguments)
            elif name == "create_issue":
                result = await issue_tools.create_issue(**arguments)
            elif name == "update_issue":
                result = await issue_tools.update_issue(**arguments)
            elif name == "add_comment":
                result = await issue_tools.add_comment(**arguments)
            elif name == "get_labels":
                result = await label_tools.get_labels(**arguments)
            elif name == "suggest_labels":
                result = await label_tools.suggest_labels(**arguments)
            elif name == "aggregate_issues":
                result = await issue_tools.aggregate_issues(**arguments)
            # Wiki tools
            elif name == "list_wiki_pages":
                result = await wiki_tools.list_wiki_pages(**arguments)
            elif name == "get_wiki_page":
                result = await wiki_tools.get_wiki_page(**arguments)
            elif name == "create_wiki_page":
                result = await wiki_tools.create_wiki_page(**arguments)
            elif name == "update_wiki_page":
                result = await wiki_tools.update_wiki_page(**arguments)
            elif name == "create_lesson":
                result = await wiki_tools.create_lesson(**arguments)
            elif name == "search_lessons":
                tags = arguments.get('tags')
                result = await wiki_tools.search_lessons(
                    query=arguments.get('query'),
                    tags=tags,
                    limit=arguments.get('limit', 20),
                    repo=arguments.get('repo')
                )
            elif name == "allocate_rfc_number":
                result = await wiki_tools.allocate_rfc_number(
                    repo=arguments.get('repo')
                )
            # Milestone tools
            elif name == "list_milestones":
                result = await milestone_tools.list_milestones(**arguments)
            elif name == "get_milestone":
                result = await milestone_tools.get_milestone(**arguments)
            elif name == "create_milestone":
                result = await milestone_tools.create_milestone(**arguments)
            elif name == "update_milestone":
                result = await milestone_tools.update_milestone(**arguments)
            elif name == "delete_milestone":
                result = await milestone_tools.delete_milestone(**arguments)
            # Dependency tools
            elif name == "list_issue_dependencies":
                result = await dependency_tools.list_issue_dependencies(**arguments)
            elif name == "create_issue_dependency":
                result = await dependency_tools.create_issue_dependency(**arguments)
            elif name == "remove_issue_dependency":
                result = await dependency_tools.remove_issue_dependency(**arguments)
            elif name == "get_execution_order":
                result = await dependency_tools.get_execution_order(**arguments)
            # Validation tools
            elif name == "validate_repo_org":
                is_org = client.is_org_repo(arguments.get('repo'))
                result = {'is_organization': is_org}
            elif name == "get_branch_protection":
                result = client.get_branch_protection(
                    arguments['branch'],
                    arguments.get('repo')
                )
            elif name == "create_label":
                result = client.create_label(
                    arguments['name'],
                    arguments['color'],
                    arguments.get('description'),
                    arguments.get('repo')
                )
            elif name == "create_org_label":
                result = client.create_org_label(
                    arguments['org'],
                    arguments['name'],
                    arguments['color'],
                    arguments.get('description')
                )
            elif name == "create_label_smart":
                result = await label_tools.create_label_smart(
                    arguments['name'],
                    arguments['color'],
                    arguments.get('description'),
                    arguments.get('repo')
                )
            # Pull Request tools
            elif name == "list_pull_requests":
                result = await pr_tools.list_pull_requests(**arguments)
            elif name == "get_pull_request":
                result = await pr_tools.get_pull_request(**arguments)
            elif name == "get_pr_diff":
                result = await pr_tools.get_pr_diff(**arguments)
            elif name == "get_pr_comments":
                result = await pr_tools.get_pr_comments(**arguments)
            elif name == "create_pr_review":
                result = await pr_tools.create_pr_review(**arguments)
            elif name == "add_pr_comment":
                result = await pr_tools.add_pr_comment(**arguments)
            elif name == "create_pull_request":
                result = await pr_tools.create_pull_request(**arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        except Exception as e:
            logger.error(f"Tool {name} failed: {e}")
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]

    return dispatch
