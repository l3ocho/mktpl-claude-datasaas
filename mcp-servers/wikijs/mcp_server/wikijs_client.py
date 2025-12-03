"""
Wiki.js GraphQL API Client.

Provides methods for interacting with Wiki.js GraphQL API for page management,
lessons learned, and documentation.
"""
import httpx
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class WikiJSClient:
    """Client for Wiki.js GraphQL API"""

    def __init__(self, api_url: str, api_token: str, base_path: str, project: Optional[str] = None):
        """
        Initialize Wiki.js client.

        Args:
            api_url: Wiki.js GraphQL API URL (e.g., http://wiki.example.com/graphql)
            api_token: Wiki.js API token
            base_path: Base path in Wiki.js (e.g., /hyper-hive-labs)
            project: Project path (e.g., projects/cuisineflow) for project mode
        """
        self.api_url = api_url
        self.api_token = api_token
        self.base_path = base_path.rstrip('/')
        self.project = project
        self.mode = 'project' if project else 'company'

        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

    def _get_full_path(self, relative_path: str) -> str:
        """
        Construct full path based on mode.

        Args:
            relative_path: Path relative to project or base

        Returns:
            Full path in Wiki.js
        """
        relative_path = relative_path.lstrip('/')

        if self.mode == 'project' and self.project:
            # Project mode: base_path/project/relative_path
            return f"{self.base_path}/{self.project}/{relative_path}"
        else:
            # Company mode: base_path/relative_path
            return f"{self.base_path}/{relative_path}"

    async def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute GraphQL query.

        Args:
            query: GraphQL query string
            variables: Query variables

        Returns:
            Response data

        Raises:
            httpx.HTTPError: On HTTP errors
            ValueError: On GraphQL errors
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json={'query': query, 'variables': variables or {}}
            )

            # Log response for debugging
            if response.status_code != 200:
                logger.error(f"HTTP {response.status_code}: {response.text}")

            response.raise_for_status()

            data = response.json()

            if 'errors' in data:
                errors = data['errors']
                error_messages = [err.get('message', str(err)) for err in errors]
                raise ValueError(f"GraphQL errors: {', '.join(error_messages)}")

            return data.get('data', {})

    async def search_pages(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search pages by keywords and tags.

        Args:
            query: Search query string
            tags: Filter by tags
            limit: Maximum results to return

        Returns:
            List of matching pages
        """
        graphql_query = """
        query SearchPages($query: String!) {
          pages {
            search(query: $query) {
              results {
                id
                path
                title
                description
              }
            }
          }
        }
        """

        data = await self._execute_query(graphql_query, {'query': query})
        results = data.get('pages', {}).get('search', {}).get('results', [])

        # Filter by tags if specified
        if tags:
            tags_lower = [t.lower() for t in tags]
            results = [
                r for r in results
                if any(tag.lower() in tags_lower for tag in r.get('tags', []))
            ]

        return results[:limit]

    async def get_page(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get specific page by path.

        Args:
            path: Page path (can be relative or absolute)

        Returns:
            Page data or None if not found
        """
        # Convert to absolute path
        if not path.startswith(self.base_path):
            path = self._get_full_path(path)

        graphql_query = """
        query GetPage($path: String!) {
          pages {
            single(path: $path) {
              id
              path
              title
              description
              content
              tags
              createdAt
              updatedAt
              author
              isPublished
            }
          }
        }
        """

        try:
            data = await self._execute_query(graphql_query, {'path': path})
            return data.get('pages', {}).get('single')
        except (httpx.HTTPError, ValueError) as e:
            logger.warning(f"Page not found at {path}: {e}")
            return None

    async def create_page(
        self,
        path: str,
        title: str,
        content: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        is_published: bool = True
    ) -> Dict[str, Any]:
        """
        Create new page.

        Args:
            path: Page path (relative to project/base)
            title: Page title
            content: Page content (markdown)
            description: Page description
            tags: Page tags
            is_published: Whether to publish immediately

        Returns:
            Created page data
        """
        full_path = self._get_full_path(path)

        graphql_query = """
        mutation CreatePage($path: String!, $title: String!, $content: String!, $description: String!, $tags: [String]!, $isPublished: Boolean!, $isPrivate: Boolean!) {
          pages {
            create(
              path: $path
              title: $title
              content: $content
              description: $description
              tags: $tags
              isPublished: $isPublished
              isPrivate: $isPrivate
              editor: "markdown"
              locale: "en"
            ) {
              responseResult {
                succeeded
                errorCode
                slug
                message
              }
              page {
                id
                path
                title
              }
            }
          }
        }
        """

        variables = {
            'path': full_path,
            'title': title,
            'content': content,
            'description': description,
            'tags': tags or [],
            'isPublished': is_published,
            'isPrivate': False  # Default to not private
        }

        data = await self._execute_query(graphql_query, variables)
        result = data.get('pages', {}).get('create', {})

        if not result.get('responseResult', {}).get('succeeded'):
            error_msg = result.get('responseResult', {}).get('message', 'Unknown error')
            raise ValueError(f"Failed to create page: {error_msg}")

        return result.get('page', {})

    async def update_page(
        self,
        page_id: int,
        content: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_published: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update existing page.

        Args:
            page_id: Page ID
            content: New content (if changing)
            title: New title (if changing)
            description: New description (if changing)
            tags: New tags (if changing)
            is_published: New publish status (if changing)

        Returns:
            Updated page data
        """
        # Build update fields dynamically
        fields = []
        variables = {'id': page_id}

        if content is not None:
            fields.append('content: $content')
            variables['content'] = content

        if title is not None:
            fields.append('title: $title')
            variables['title'] = title

        if description is not None:
            fields.append('description: $description')
            variables['description'] = description

        if tags is not None:
            fields.append('tags: $tags')
            variables['tags'] = tags

        if is_published is not None:
            fields.append('isPublished: $isPublished')
            variables['isPublished'] = is_published

        fields_str = ', '.join(fields)

        graphql_query = f"""
        mutation UpdatePage($id: Int!{''.join([f', ${k}: {type(v).__name__.title()}' for k, v in variables.items() if k != 'id'])}) {{
          pages {{
            update(
              id: $id
              {fields_str}
            ) {{
              responseResult {{
                succeeded
                errorCode
                message
              }}
              page {{
                id
                path
                title
                updatedAt
              }}
            }}
          }}
        }}
        """

        data = await self._execute_query(graphql_query, variables)
        result = data.get('pages', {}).get('update', {})

        if not result.get('responseResult', {}).get('succeeded'):
            error_msg = result.get('responseResult', {}).get('message', 'Unknown error')
            raise ValueError(f"Failed to update page: {error_msg}")

        return result.get('page', {})

    async def list_pages(self, path_prefix: str = "") -> List[Dict[str, Any]]:
        """
        List pages under a specific path.

        Args:
            path_prefix: Path prefix to filter (relative to project/base)

        Returns:
            List of pages
        """
        # Construct full path based on mode
        if path_prefix:
            full_path = self._get_full_path(path_prefix)
        else:
            # Empty path_prefix: return all pages in project (project mode) or base (company mode)
            if self.mode == 'project' and self.project:
                full_path = f"{self.base_path}/{self.project}"
            else:
                full_path = self.base_path

        graphql_query = """
        query ListPages {
          pages {
            list {
              id
              path
              title
              description
              tags
              createdAt
              updatedAt
              isPublished
            }
          }
        }
        """

        data = await self._execute_query(graphql_query)
        all_pages = data.get('pages', {}).get('list', [])

        # Filter by path prefix
        if full_path:
            return [p for p in all_pages if p.get('path', '').startswith(full_path)]

        return all_pages

    async def create_lesson(
        self,
        title: str,
        content: str,
        tags: List[str],
        category: str = "sprints"
    ) -> Dict[str, Any]:
        """
        Create a lessons learned entry.

        Args:
            title: Lesson title
            content: Lesson content (markdown)
            tags: Tags for categorization
            category: Category (sprints, patterns, etc.)

        Returns:
            Created lesson page data
        """
        # Construct path: lessons-learned/category/title-slug
        slug = title.lower().replace(' ', '-').replace('_', '-')
        path = f"lessons-learned/{category}/{slug}"

        return await self.create_page(
            path=path,
            title=title,
            content=content,
            description=f"Lessons learned: {title}",
            tags=tags + ['lesson-learned', category],
            is_published=True
        )

    async def search_lessons(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search lessons learned entries.

        Args:
            query: Search query (optional)
            tags: Filter by tags
            limit: Maximum results

        Returns:
            List of matching lessons
        """
        # Search in lessons-learned path
        search_query = query or "lesson"

        results = await self.search_pages(search_query, tags, limit)

        # Filter to only lessons-learned path
        lessons_path = self._get_full_path("lessons-learned")
        return [r for r in results if r.get('path', '').startswith(lessons_path)]

    async def tag_lesson(self, page_id: int, new_tags: List[str]) -> Dict[str, Any]:
        """
        Add tags to a lesson.

        Args:
            page_id: Lesson page ID
            new_tags: Tags to add

        Returns:
            Updated page data
        """
        # Get current page to merge tags
        # For now, just replace tags (can enhance to merge later)
        return await self.update_page(page_id=page_id, tags=new_tags)
