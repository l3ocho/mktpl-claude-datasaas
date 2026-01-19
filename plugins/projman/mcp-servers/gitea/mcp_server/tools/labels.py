"""
Label management tools for MCP server.

Provides async wrappers for label operations with:
- Label taxonomy retrieval
- Intelligent label suggestion
- Dynamic label detection
"""
import asyncio
import logging
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
        """Get all labels (org + repo). Repo must be 'owner/repo' format."""
        loop = asyncio.get_event_loop()

        target_repo = repo or self.gitea.repo
        if not target_repo or '/' not in target_repo:
            raise ValueError("Use 'owner/repo' format (e.g. 'org/repo-name')")

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

    async def suggest_labels(self, context: str) -> List[str]:
        """
        Analyze context and suggest appropriate labels.

        Args:
            context: Issue title + description or sprint context

        Returns:
            List of suggested label names
        """
        suggested = []
        context_lower = context.lower()

        # Type detection (exclusive - only one)
        if any(word in context_lower for word in ['bug', 'error', 'fix', 'broken', 'crash', 'fail']):
            suggested.append('Type/Bug')
        elif any(word in context_lower for word in ['refactor', 'extract', 'restructure', 'architecture', 'service extraction']):
            suggested.append('Type/Refactor')
        elif any(word in context_lower for word in ['feature', 'add', 'implement', 'new', 'create']):
            suggested.append('Type/Feature')
        elif any(word in context_lower for word in ['docs', 'documentation', 'readme', 'guide']):
            suggested.append('Type/Documentation')
        elif any(word in context_lower for word in ['test', 'testing', 'spec', 'coverage']):
            suggested.append('Type/Test')
        elif any(word in context_lower for word in ['chore', 'maintenance', 'update', 'upgrade']):
            suggested.append('Type/Chore')

        # Priority detection
        if any(word in context_lower for word in ['critical', 'urgent', 'blocker', 'blocking', 'emergency']):
            suggested.append('Priority/Critical')
        elif any(word in context_lower for word in ['high', 'important', 'asap', 'soon']):
            suggested.append('Priority/High')
        elif any(word in context_lower for word in ['low', 'nice-to-have', 'optional', 'later']):
            suggested.append('Priority/Low')
        else:
            suggested.append('Priority/Medium')

        # Complexity detection
        if any(word in context_lower for word in ['simple', 'trivial', 'easy', 'quick']):
            suggested.append('Complexity/Simple')
        elif any(word in context_lower for word in ['complex', 'difficult', 'challenging', 'intricate']):
            suggested.append('Complexity/Complex')
        else:
            suggested.append('Complexity/Medium')

        # Efforts detection
        if any(word in context_lower for word in ['xs', 'tiny', '1 hour', '2 hours']):
            suggested.append('Efforts/XS')
        elif any(word in context_lower for word in ['small', 's ', '1 day', 'half day']):
            suggested.append('Efforts/S')
        elif any(word in context_lower for word in ['medium', 'm ', '2 days', '3 days']):
            suggested.append('Efforts/M')
        elif any(word in context_lower for word in ['large', 'l ', '1 week', '5 days']):
            suggested.append('Efforts/L')
        elif any(word in context_lower for word in ['xl', 'extra large', '2 weeks', 'sprint']):
            suggested.append('Efforts/XL')

        # Component detection (based on keywords)
        component_keywords = {
            'Component/Backend': ['backend', 'server', 'api', 'database', 'service'],
            'Component/Frontend': ['frontend', 'ui', 'interface', 'react', 'vue', 'component'],
            'Component/API': ['api', 'endpoint', 'rest', 'graphql', 'route'],
            'Component/Database': ['database', 'db', 'sql', 'migration', 'schema', 'postgres'],
            'Component/Auth': ['auth', 'authentication', 'login', 'oauth', 'token', 'session'],
            'Component/Deploy': ['deploy', 'deployment', 'docker', 'kubernetes', 'ci/cd'],
            'Component/Testing': ['test', 'testing', 'spec', 'jest', 'pytest', 'coverage'],
            'Component/Docs': ['docs', 'documentation', 'readme', 'guide', 'wiki']
        }

        for label, keywords in component_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                suggested.append(label)

        # Tech stack detection
        tech_keywords = {
            'Tech/Python': ['python', 'fastapi', 'django', 'flask', 'pytest'],
            'Tech/JavaScript': ['javascript', 'js', 'node', 'npm', 'yarn'],
            'Tech/Docker': ['docker', 'dockerfile', 'container', 'compose'],
            'Tech/PostgreSQL': ['postgres', 'postgresql', 'psql', 'sql'],
            'Tech/Redis': ['redis', 'cache', 'session store'],
            'Tech/Vue': ['vue', 'vuejs', 'nuxt'],
            'Tech/FastAPI': ['fastapi', 'pydantic', 'starlette']
        }

        for label, keywords in tech_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                suggested.append(label)

        # Source detection (based on git branch or context)
        if 'development' in context_lower or 'dev/' in context_lower:
            suggested.append('Source/Development')
        elif 'staging' in context_lower or 'stage/' in context_lower:
            suggested.append('Source/Staging')
        elif 'production' in context_lower or 'prod' in context_lower:
            suggested.append('Source/Production')

        # Risk detection
        if any(word in context_lower for word in ['breaking', 'breaking change', 'major', 'risky']):
            suggested.append('Risk/High')
        elif any(word in context_lower for word in ['safe', 'low risk', 'minor']):
            suggested.append('Risk/Low')

        logger.info(f"Suggested {len(suggested)} labels based on context")
        return suggested
