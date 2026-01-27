"""
MCP Server entry point for Gitea integration.

Provides Gitea tools to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import GiteaConfig
from .gitea_client import GiteaClient
from .tools.issues import IssueTools
from .tools.labels import LabelTools
from .tools.wiki import WikiTools
from .tools.milestones import MilestoneTools
from .tools.dependencies import DependencyTools
from .tools.pull_requests import PullRequestTools

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class GiteaMCPServer:
    """MCP Server for Gitea integration"""

    def __init__(self):
        self.server = Server("gitea-mcp")
        self.config = None
        self.client = None
        self.issue_tools = None
        self.label_tools = None
        self.wiki_tools = None
        self.milestone_tools = None
        self.dependency_tools = None
        self.pr_tools = None

    async def initialize(self):
        """
        Initialize server and load configuration.

        Raises:
            Exception: If initialization fails
        """
        try:
            config_loader = GiteaConfig()
            self.config = config_loader.load()

            self.client = GiteaClient()
            self.issue_tools = IssueTools(self.client)
            self.label_tools = LabelTools(self.client)
            self.wiki_tools = WikiTools(self.client)
            self.milestone_tools = MilestoneTools(self.client)
            self.dependency_tools = DependencyTools(self.client)
            self.pr_tools = PullRequestTools(self.client)

            logger.info(f"Gitea MCP Server initialized in {self.config['mode']} mode")
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
                                "description": "Issue that will depend on another"
                            },
                            "depends_on": {
                                "type": "integer",
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
                                "type": "integer",
                                "description": "Issue that depends on another"
                            },
                            "depends_on": {
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                "type": "integer",
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
                                        "position": {"type": "integer"},
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
                                "type": "integer",
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

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """
            Handle tool invocation.

            Args:
                name: Tool name
                arguments: Tool arguments

            Returns:
                List of TextContent with results
            """
            try:
                # Route to appropriate tool handler
                if name == "list_issues":
                    result = await self.issue_tools.list_issues(**arguments)
                elif name == "get_issue":
                    result = await self.issue_tools.get_issue(**arguments)
                elif name == "create_issue":
                    result = await self.issue_tools.create_issue(**arguments)
                elif name == "update_issue":
                    result = await self.issue_tools.update_issue(**arguments)
                elif name == "add_comment":
                    result = await self.issue_tools.add_comment(**arguments)
                elif name == "get_labels":
                    result = await self.label_tools.get_labels(**arguments)
                elif name == "suggest_labels":
                    result = await self.label_tools.suggest_labels(**arguments)
                elif name == "aggregate_issues":
                    result = await self.issue_tools.aggregate_issues(**arguments)
                # Wiki tools
                elif name == "list_wiki_pages":
                    result = await self.wiki_tools.list_wiki_pages(**arguments)
                elif name == "get_wiki_page":
                    result = await self.wiki_tools.get_wiki_page(**arguments)
                elif name == "create_wiki_page":
                    result = await self.wiki_tools.create_wiki_page(**arguments)
                elif name == "update_wiki_page":
                    result = await self.wiki_tools.update_wiki_page(**arguments)
                elif name == "create_lesson":
                    result = await self.wiki_tools.create_lesson(**arguments)
                elif name == "search_lessons":
                    tags = arguments.get('tags')
                    result = await self.wiki_tools.search_lessons(
                        query=arguments.get('query'),
                        tags=tags,
                        limit=arguments.get('limit', 20),
                        repo=arguments.get('repo')
                    )
                # Milestone tools
                elif name == "list_milestones":
                    result = await self.milestone_tools.list_milestones(**arguments)
                elif name == "get_milestone":
                    result = await self.milestone_tools.get_milestone(**arguments)
                elif name == "create_milestone":
                    result = await self.milestone_tools.create_milestone(**arguments)
                elif name == "update_milestone":
                    result = await self.milestone_tools.update_milestone(**arguments)
                elif name == "delete_milestone":
                    result = await self.milestone_tools.delete_milestone(**arguments)
                # Dependency tools
                elif name == "list_issue_dependencies":
                    result = await self.dependency_tools.list_issue_dependencies(**arguments)
                elif name == "create_issue_dependency":
                    result = await self.dependency_tools.create_issue_dependency(**arguments)
                elif name == "remove_issue_dependency":
                    result = await self.dependency_tools.remove_issue_dependency(**arguments)
                elif name == "get_execution_order":
                    result = await self.dependency_tools.get_execution_order(**arguments)
                # Validation tools
                elif name == "validate_repo_org":
                    is_org = self.client.is_org_repo(arguments.get('repo'))
                    result = {'is_organization': is_org}
                elif name == "get_branch_protection":
                    result = self.client.get_branch_protection(
                        arguments['branch'],
                        arguments.get('repo')
                    )
                elif name == "create_label":
                    result = self.client.create_label(
                        arguments['name'],
                        arguments['color'],
                        arguments.get('description'),
                        arguments.get('repo')
                    )
                elif name == "create_org_label":
                    result = self.client.create_org_label(
                        arguments['org'],
                        arguments['name'],
                        arguments['color'],
                        arguments.get('description')
                    )
                elif name == "create_label_smart":
                    result = await self.label_tools.create_label_smart(
                        arguments['name'],
                        arguments['color'],
                        arguments.get('description'),
                        arguments.get('repo')
                    )
                # Pull Request tools
                elif name == "list_pull_requests":
                    result = await self.pr_tools.list_pull_requests(**arguments)
                elif name == "get_pull_request":
                    result = await self.pr_tools.get_pull_request(**arguments)
                elif name == "get_pr_diff":
                    result = await self.pr_tools.get_pr_diff(**arguments)
                elif name == "get_pr_comments":
                    result = await self.pr_tools.get_pr_comments(**arguments)
                elif name == "create_pr_review":
                    result = await self.pr_tools.create_pr_review(**arguments)
                elif name == "add_pr_comment":
                    result = await self.pr_tools.add_pr_comment(**arguments)
                elif name == "create_pull_request":
                    result = await self.pr_tools.create_pull_request(**arguments)
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

    async def run(self):
        """Run the MCP server"""
        await self.initialize()
        self.setup_tools()

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = GiteaMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
