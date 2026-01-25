"""
Configuration loader for Data Platform MCP Server.

Implements hybrid configuration system:
- System-level: ~/.config/claude/postgres.env (credentials)
- Project-level: .env (dbt project paths, overrides)
- Auto-detection: dbt_project.yml discovery
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPlatformConfig:
    """Hybrid configuration loader for data platform tools"""

    def __init__(self):
        self.postgres_url: Optional[str] = None
        self.dbt_project_dir: Optional[str] = None
        self.dbt_profiles_dir: Optional[str] = None
        self.max_rows: int = 100_000

    def load(self) -> Dict[str, Optional[str]]:
        """
        Load configuration from system and project levels.

        Returns:
            Dict containing postgres_url, dbt_project_dir, dbt_profiles_dir, max_rows

        Note:
            PostgreSQL credentials are optional - server can run in pandas-only mode.
        """
        # Load system config (PostgreSQL credentials)
        system_config = Path.home() / '.config' / 'claude' / 'postgres.env'
        if system_config.exists():
            load_dotenv(system_config)
            logger.info(f"Loaded system configuration from {system_config}")
        else:
            logger.info(
                f"System config not found: {system_config} - "
                "PostgreSQL tools will be unavailable"
            )

        # Find project directory
        project_dir = self._find_project_directory()

        # Load project config (overrides system)
        if project_dir:
            project_config = project_dir / '.env'
            if project_config.exists():
                load_dotenv(project_config, override=True)
                logger.info(f"Loaded project configuration from {project_config}")

        # Extract values
        self.postgres_url = os.getenv('POSTGRES_URL')
        self.dbt_project_dir = os.getenv('DBT_PROJECT_DIR')
        self.dbt_profiles_dir = os.getenv('DBT_PROFILES_DIR')
        self.max_rows = int(os.getenv('DATA_PLATFORM_MAX_ROWS', '100000'))

        # Auto-detect dbt project if not specified
        if not self.dbt_project_dir and project_dir:
            self.dbt_project_dir = self._find_dbt_project(project_dir)
            if self.dbt_project_dir:
                logger.info(f"Auto-detected dbt project: {self.dbt_project_dir}")

        # Default dbt profiles dir to ~/.dbt
        if not self.dbt_profiles_dir:
            default_profiles = Path.home() / '.dbt'
            if default_profiles.exists():
                self.dbt_profiles_dir = str(default_profiles)

        return {
            'postgres_url': self.postgres_url,
            'dbt_project_dir': self.dbt_project_dir,
            'dbt_profiles_dir': self.dbt_profiles_dir,
            'max_rows': self.max_rows,
            'postgres_available': self.postgres_url is not None,
            'dbt_available': self.dbt_project_dir is not None
        }

    def _find_project_directory(self) -> Optional[Path]:
        """
        Find the user's project directory.

        Returns:
            Path to project directory, or None if not found
        """
        # Strategy 1: Check CLAUDE_PROJECT_DIR environment variable
        project_dir = os.getenv('CLAUDE_PROJECT_DIR')
        if project_dir:
            path = Path(project_dir)
            if path.exists():
                logger.info(f"Found project directory from CLAUDE_PROJECT_DIR: {path}")
                return path

        # Strategy 2: Check PWD
        pwd = os.getenv('PWD')
        if pwd:
            path = Path(pwd)
            if path.exists() and (
                (path / '.git').exists() or
                (path / '.env').exists() or
                (path / 'dbt_project.yml').exists()
            ):
                logger.info(f"Found project directory from PWD: {path}")
                return path

        # Strategy 3: Check current working directory
        cwd = Path.cwd()
        if (cwd / '.git').exists() or (cwd / '.env').exists() or (cwd / 'dbt_project.yml').exists():
            logger.info(f"Found project directory from cwd: {cwd}")
            return cwd

        logger.debug("Could not determine project directory")
        return None

    def _find_dbt_project(self, start_dir: Path) -> Optional[str]:
        """
        Find dbt_project.yml in the project or its subdirectories.

        Args:
            start_dir: Directory to start searching from

        Returns:
            Path to dbt project directory, or None if not found
        """
        # Check root
        if (start_dir / 'dbt_project.yml').exists():
            return str(start_dir)

        # Check common subdirectories
        for subdir in ['dbt', 'transform', 'analytics', 'models']:
            candidate = start_dir / subdir
            if (candidate / 'dbt_project.yml').exists():
                return str(candidate)

        # Search one level deep
        for item in start_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if (item / 'dbt_project.yml').exists():
                    return str(item)

        return None


def load_config() -> Dict[str, Optional[str]]:
    """
    Convenience function to load configuration.

    Returns:
        Configuration dictionary
    """
    config = DataPlatformConfig()
    return config.load()


def check_postgres_connection() -> Dict[str, any]:
    """
    Check PostgreSQL connection status for SessionStart hook.

    Returns:
        Dict with connection status and message
    """
    import asyncio

    config = load_config()
    if not config.get('postgres_url'):
        return {
            'connected': False,
            'message': 'PostgreSQL not configured (POSTGRES_URL not set)'
        }

    async def test_connection():
        try:
            import asyncpg
            conn = await asyncpg.connect(config['postgres_url'], timeout=5)
            version = await conn.fetchval('SELECT version()')
            await conn.close()
            return {
                'connected': True,
                'message': f'Connected to PostgreSQL',
                'version': version.split(',')[0] if version else 'Unknown'
            }
        except Exception as e:
            return {
                'connected': False,
                'message': f'PostgreSQL connection failed: {str(e)}'
            }

    return asyncio.run(test_connection())
