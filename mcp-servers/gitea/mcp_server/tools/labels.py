"""
Label management tools for MCP server.

Provides async wrappers for label operations with:
- Label taxonomy retrieval
- Intelligent label suggestion
- Dynamic label detection
"""
import asyncio
import logging
import re
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LabelTools:
    """Async wrappers for Gitea label operations"""

    def __init__(self, gitea_client):
        """
        Initialize label tools.

        Args:
            gitea_client: GiteaClient instance
        """
        self.gitea = gitea_client

    async def get_labels(self, repo: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Get all labels (org + repo if org-owned, repo-only if user-owned)."""
        loop = asyncio.get_event_loop()

        target_repo = repo or self.gitea.repo
        if not target_repo or '/' not in target_repo:
            raise ValueError("Use 'owner/repo' format (e.g. 'org/repo-name')")

        # Check if repo belongs to an organization or user
        is_org = await loop.run_in_executor(
            None,
            lambda: self.gitea.is_org_repo(target_repo)
        )

        org_labels = []
        if is_org:
            org = target_repo.split('/')[0]
            org_labels = await loop.run_in_executor(
                None,
                lambda: self.gitea.get_org_labels(org)
            )

        repo_labels = await loop.run_in_executor(
            None,
            lambda: self.gitea.get_labels(target_repo)
        )

        return {
            'organization': org_labels,
            'repository': repo_labels,
            'total_count': len(org_labels) + len(repo_labels)
        }

    async def suggest_labels(self, context: str, repo: Optional[str] = None) -> List[str]:
        """
        Analyze context and suggest appropriate labels from repository's actual labels.

        This method fetches actual labels from the repository and matches them
        dynamically, supporting any label naming convention (slash, colon-space, etc.).

        Args:
            context: Issue title + description or sprint context
            repo: Repository in 'owner/repo' format (optional, uses default if not provided)

        Returns:
            List of suggested label names that exist in the repository
        """
        # Fetch actual labels from repository
        target_repo = repo or self.gitea.repo
        if not target_repo:
            logger.warning("No repository specified, returning empty suggestions")
            return []

        try:
            labels_data = await self.get_labels(target_repo)
            all_labels = labels_data.get('organization', []) + labels_data.get('repository', [])
            label_names = [label['name'] for label in all_labels]
        except Exception as e:
            logger.warning(f"Failed to fetch labels: {e}. Using fallback suggestions.")
            label_names = []

        # Build label lookup for dynamic matching
        label_lookup = self._build_label_lookup(label_names)

        suggested = []
        context_lower = context.lower()

        # Type detection (exclusive - only one)
        type_label = None
        if any(word in context_lower for word in ['bug', 'error', 'fix', 'broken', 'crash', 'fail']):
            type_label = self._find_label(label_lookup, 'type', 'bug')
        elif any(word in context_lower for word in ['refactor', 'extract', 'restructure', 'architecture', 'service extraction']):
            type_label = self._find_label(label_lookup, 'type', 'refactor')
        elif any(word in context_lower for word in ['feature', 'add', 'implement', 'new', 'create']):
            type_label = self._find_label(label_lookup, 'type', 'feature')
        elif any(word in context_lower for word in ['docs', 'documentation', 'readme', 'guide']):
            type_label = self._find_label(label_lookup, 'type', 'documentation')
        elif any(word in context_lower for word in ['test', 'testing', 'spec', 'coverage']):
            type_label = self._find_label(label_lookup, 'type', 'test')
        elif any(word in context_lower for word in ['chore', 'maintenance', 'update', 'upgrade']):
            type_label = self._find_label(label_lookup, 'type', 'chore')
        if type_label:
            suggested.append(type_label)

        # Priority detection
        priority_label = None
        if any(word in context_lower for word in ['critical', 'urgent', 'blocker', 'blocking', 'emergency']):
            priority_label = self._find_label(label_lookup, 'priority', 'critical')
        elif any(word in context_lower for word in ['high', 'important', 'asap', 'soon']):
            priority_label = self._find_label(label_lookup, 'priority', 'high')
        elif any(word in context_lower for word in ['low', 'nice-to-have', 'optional', 'later']):
            priority_label = self._find_label(label_lookup, 'priority', 'low')
        else:
            priority_label = self._find_label(label_lookup, 'priority', 'medium')
        if priority_label:
            suggested.append(priority_label)

        # Complexity detection
        complexity_label = None
        if any(word in context_lower for word in ['simple', 'trivial', 'easy', 'quick']):
            complexity_label = self._find_label(label_lookup, 'complexity', 'simple')
        elif any(word in context_lower for word in ['complex', 'difficult', 'challenging', 'intricate']):
            complexity_label = self._find_label(label_lookup, 'complexity', 'complex')
        else:
            complexity_label = self._find_label(label_lookup, 'complexity', 'medium')
        if complexity_label:
            suggested.append(complexity_label)

        # Effort detection (supports both "Effort" and "Efforts" naming)
        effort_label = None
        if any(word in context_lower for word in ['xs', 'tiny', '1 hour', '2 hours']):
            effort_label = self._find_label(label_lookup, 'effort', 'xs')
        elif any(word in context_lower for word in ['small', 's ', '1 day', 'half day']):
            effort_label = self._find_label(label_lookup, 'effort', 's')
        elif any(word in context_lower for word in ['medium', 'm ', '2 days', '3 days']):
            effort_label = self._find_label(label_lookup, 'effort', 'm')
        elif any(word in context_lower for word in ['large', 'l ', '1 week', '5 days']):
            effort_label = self._find_label(label_lookup, 'effort', 'l')
        elif any(word in context_lower for word in ['xl', 'extra large', '2 weeks', 'sprint']):
            effort_label = self._find_label(label_lookup, 'effort', 'xl')
        if effort_label:
            suggested.append(effort_label)

        # Component detection (based on keywords)
        component_mappings = {
            'backend': ['backend', 'server', 'api', 'database', 'service'],
            'frontend': ['frontend', 'ui', 'interface', 'react', 'vue', 'component'],
            'api': ['api', 'endpoint', 'rest', 'graphql', 'route'],
            'database': ['database', 'db', 'sql', 'migration', 'schema', 'postgres'],
            'auth': ['auth', 'authentication', 'login', 'oauth', 'token', 'session'],
            'deploy': ['deploy', 'deployment', 'docker', 'kubernetes', 'ci/cd'],
            'testing': ['test', 'testing', 'spec', 'jest', 'pytest', 'coverage'],
            'docs': ['docs', 'documentation', 'readme', 'guide', 'wiki']
        }

        for component, keywords in component_mappings.items():
            if any(keyword in context_lower for keyword in keywords):
                label = self._find_label(label_lookup, 'component', component)
                if label and label not in suggested:
                    suggested.append(label)

        # Tech stack detection
        tech_mappings = {
            'python': ['python', 'fastapi', 'django', 'flask', 'pytest'],
            'javascript': ['javascript', 'js', 'node', 'npm', 'yarn'],
            'docker': ['docker', 'dockerfile', 'container', 'compose'],
            'postgresql': ['postgres', 'postgresql', 'psql', 'sql'],
            'redis': ['redis', 'cache', 'session store'],
            'vue': ['vue', 'vuejs', 'nuxt'],
            'fastapi': ['fastapi', 'pydantic', 'starlette']
        }

        for tech, keywords in tech_mappings.items():
            if any(keyword in context_lower for keyword in keywords):
                label = self._find_label(label_lookup, 'tech', tech)
                if label and label not in suggested:
                    suggested.append(label)

        # Source detection (based on git branch or context)
        source_label = None
        if 'development' in context_lower or 'dev/' in context_lower:
            source_label = self._find_label(label_lookup, 'source', 'development')
        elif 'staging' in context_lower or 'stage/' in context_lower:
            source_label = self._find_label(label_lookup, 'source', 'staging')
        elif 'production' in context_lower or 'prod' in context_lower:
            source_label = self._find_label(label_lookup, 'source', 'production')
        if source_label:
            suggested.append(source_label)

        # Risk detection
        risk_label = None
        if any(word in context_lower for word in ['breaking', 'breaking change', 'major', 'risky']):
            risk_label = self._find_label(label_lookup, 'risk', 'high')
        elif any(word in context_lower for word in ['safe', 'low risk', 'minor']):
            risk_label = self._find_label(label_lookup, 'risk', 'low')
        if risk_label:
            suggested.append(risk_label)

        logger.info(f"Suggested {len(suggested)} labels based on context and {len(label_names)} available labels")
        return suggested

    def _build_label_lookup(self, label_names: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Build a lookup dictionary for label matching.

        Supports various label formats:
        - Slash format: Type/Bug, Priority/High
        - Colon-space format: Type: Bug, Priority: High
        - Colon format: Type:Bug

        Args:
            label_names: List of actual label names from repository

        Returns:
            Nested dict: {category: {value: actual_label_name}}
        """
        lookup: Dict[str, Dict[str, str]] = {}

        for label in label_names:
            # Try different separator patterns
            # Pattern: Category<separator>Value
            # Separators: /, : , :
            match = re.match(r'^([^/:]+)(?:/|:\s*|:)(.+)$', label)
            if match:
                category = match.group(1).lower().rstrip('s')  # Normalize: "Efforts" -> "effort"
                value = match.group(2).lower()

                if category not in lookup:
                    lookup[category] = {}
                lookup[category][value] = label

        return lookup

    def _find_label(self, lookup: Dict[str, Dict[str, str]], category: str, value: str) -> Optional[str]:
        """
        Find actual label name from lookup.

        Args:
            lookup: Label lookup dictionary
            category: Category to search (e.g., 'type', 'priority')
            value: Value to find (e.g., 'bug', 'high')

        Returns:
            Actual label name if found, None otherwise
        """
        category_lower = category.lower().rstrip('s')  # Normalize
        value_lower = value.lower()

        if category_lower in lookup and value_lower in lookup[category_lower]:
            return lookup[category_lower][value_lower]

        return None

    # Organization-level label categories (workflow labels shared across repos)
    ORG_LABEL_CATEGORIES = {'agent', 'complexity', 'effort', 'efforts', 'priority', 'risk', 'source', 'type'}

    # Repository-level label categories (project-specific labels)
    REPO_LABEL_CATEGORIES = {'component', 'tech'}

    async def create_label_smart(
        self,
        name: str,
        color: str,
        description: Optional[str] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a label at the appropriate level (org or repo) based on category.

        Organization labels: Agent, Complexity, Effort, Priority, Risk, Source, Type
        Repository labels: Component, Tech

        Args:
            name: Label name (e.g., 'Type/Bug', 'Component/Backend')
            color: Hex color code
            description: Optional label description
            repo: Repository in 'owner/repo' format

        Returns:
            Created label dictionary with 'level' key indicating where it was created
        """
        loop = asyncio.get_event_loop()

        target_repo = repo or self.gitea.repo
        if not target_repo or '/' not in target_repo:
            raise ValueError("Use 'owner/repo' format (e.g. 'org/repo-name')")

        # Parse category from label name
        category = None
        if '/' in name:
            category = name.split('/')[0].lower().rstrip('s')
        elif ':' in name:
            category = name.split(':')[0].strip().lower().rstrip('s')

        # Determine level
        owner = target_repo.split('/')[0]
        is_org = await loop.run_in_executor(
            None,
            lambda: self.gitea.is_org_repo(target_repo)
        )

        # If it's an org repo and the category is an org-level category, create at org level
        if is_org and category in self.ORG_LABEL_CATEGORIES:
            result = await loop.run_in_executor(
                None,
                lambda: self.gitea.create_org_label(owner, name, color, description)
            )
            result['level'] = 'organization'
            logger.info(f"Created organization label '{name}' in {owner}")
        else:
            # Create at repo level
            result = await loop.run_in_executor(
                None,
                lambda: self.gitea.create_label(name, color, description, target_repo)
            )
            result['level'] = 'repository'
            logger.info(f"Created repository label '{name}' in {target_repo}")

        return result
