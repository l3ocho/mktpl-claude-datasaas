"""
MCP tools for Wiki.js lessons learned management.
"""
from typing import Dict, Any, List, Optional
from mcp.server import Tool
from ..wikijs_client import WikiJSClient
import logging

logger = logging.getLogger(__name__)


def create_lesson_tools(client: WikiJSClient) -> List[Tool]:
    """
    Create MCP tools for lessons learned management.

    Args:
        client: WikiJSClient instance

    Returns:
        List of MCP tools
    """

    async def create_lesson(
        title: str,
        content: str,
        tags: str,
        category: str = "sprints"
    ) -> Dict[str, Any]:
        """
        Create a lessons learned entry.

        After 15 sprints without systematic lesson capture, repeated mistakes occurred.
        This tool ensures lessons are captured and searchable for future sprints.

        Args:
            title: Lesson title (e.g., "Sprint 16 - Claude Code Infinite Loop on Label Validation")
            content: Lesson content in markdown (problem, solution, prevention)
            tags: Comma-separated tags (e.g., "claude-code, testing, labels, validation")
            category: Category for organization (default: "sprints", also: "patterns", "architecture")

        Returns:
            Created lesson page data

        Example:
            create_lesson(
                title="Sprint 16 - Prevent Infinite Loops in Validation",
                content="## Problem\\n\\nClaude Code entered infinite loop...\\n\\n## Solution\\n\\n...",
                tags="claude-code, testing, infinite-loop, validation",
                category="sprints"
            )
        """
        try:
            tag_list = [t.strip() for t in tags.split(',')]

            lesson = await client.create_lesson(
                title=title,
                content=content,
                tags=tag_list,
                category=category
            )

            return {
                'success': True,
                'lesson': lesson,
                'message': f'Lesson learned captured: {title}'
            }
        except Exception as e:
            logger.error(f"Error creating lesson: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def search_lessons(
        query: Optional[str] = None,
        tags: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search lessons learned entries.

        Use this at sprint start to find relevant lessons from previous sprints.
        Prevents repeating the same mistakes.

        Args:
            query: Search query (e.g., "validation", "infinite loop", "docker")
            tags: Comma-separated tags to filter by (e.g., "claude-code, testing")
            limit: Maximum number of results (default: 20)

        Returns:
            List of matching lessons learned

        Example:
            # Before implementing validation logic
            search_lessons(query="validation", tags="testing, claude-code")

            # Before working with Docker
            search_lessons(query="docker", tags="deployment")
        """
        try:
            tag_list = [t.strip() for t in tags.split(',')] if tags else None

            lessons = await client.search_lessons(
                query=query,
                tags=tag_list,
                limit=limit
            )

            return {
                'success': True,
                'count': len(lessons),
                'lessons': lessons,
                'message': f'Found {len(lessons)} relevant lessons'
            }
        except Exception as e:
            logger.error(f"Error searching lessons: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def tag_lesson(
        page_id: int,
        tags: str
    ) -> Dict[str, Any]:
        """
        Add or update tags on a lesson.

        Args:
            page_id: Lesson page ID (from create_lesson or search_lessons)
            tags: Comma-separated tags (will replace existing tags)

        Returns:
            Updated lesson data
        """
        try:
            tag_list = [t.strip() for t in tags.split(',')]

            lesson = await client.tag_lesson(
                page_id=page_id,
                new_tags=tag_list
            )

            return {
                'success': True,
                'lesson': lesson,
                'message': 'Tags updated successfully'
            }
        except Exception as e:
            logger.error(f"Error tagging lesson: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # Define MCP tools
    tools = [
        Tool(
            name="create_lesson",
            description=(
                "Create a lessons learned entry to prevent repeating mistakes. "
                "Critical for capturing sprint insights, architectural decisions, "
                "and technical gotchas for future reference."
            ),
            function=create_lesson
        ),
        Tool(
            name="search_lessons",
            description=(
                "Search lessons learned from previous sprints and projects. "
                "Use this before starting new work to avoid known pitfalls and "
                "leverage past solutions."
            ),
            function=search_lessons
        ),
        Tool(
            name="tag_lesson",
            description="Add or update tags on a lessons learned entry for better categorization",
            function=tag_lesson
        )
    ]

    return tools
