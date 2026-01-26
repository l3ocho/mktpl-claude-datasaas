"""
Configuration loader for viz-platform MCP Server.

Implements hybrid configuration system:
- System-level: ~/.config/claude/viz-platform.env (theme preferences)
- Project-level: .env (DMC version overrides)
- Auto-detection: DMC package version from installed package
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VizPlatformConfig:
    """Hybrid configuration loader for viz-platform tools"""

    def __init__(self):
        self.dmc_version: Optional[str] = None
        self.theme_dir_user: Path = Path.home() / '.config' / 'claude' / 'themes'
        self.theme_dir_project: Optional[Path] = None
        self.default_theme: Optional[str] = None

    def load(self) -> Dict[str, any]:
        """
        Load configuration from system and project levels.

        Returns:
            Dict containing dmc_version, theme directories, and availability flags
        """
        # Load system config
        system_config = Path.home() / '.config' / 'claude' / 'viz-platform.env'
        if system_config.exists():
            load_dotenv(system_config)
            logger.info(f"Loaded system configuration from {system_config}")

        # Find project directory
        project_dir = self._find_project_directory()

        # Load project config (overrides system)
        if project_dir:
            project_config = project_dir / '.env'
            if project_config.exists():
                load_dotenv(project_config, override=True)
                logger.info(f"Loaded project configuration from {project_config}")

            # Set project theme directory
            self.theme_dir_project = project_dir / '.viz-platform' / 'themes'

        # Get DMC version (from env or auto-detect)
        self.dmc_version = os.getenv('DMC_VERSION') or self._detect_dmc_version()
        self.default_theme = os.getenv('VIZ_DEFAULT_THEME')

        # Ensure user theme directory exists
        self.theme_dir_user.mkdir(parents=True, exist_ok=True)

        return {
            'dmc_version': self.dmc_version,
            'dmc_available': self.dmc_version is not None,
            'theme_dir_user': str(self.theme_dir_user),
            'theme_dir_project': str(self.theme_dir_project) if self.theme_dir_project else None,
            'default_theme': self.default_theme,
            'project_dir': str(project_dir) if project_dir else None
        }

    def _detect_dmc_version(self) -> Optional[str]:
        """
        Auto-detect installed Dash Mantine Components version.

        Returns:
            Version string (e.g., "0.14.7") or None if not installed
        """
        try:
            from importlib.metadata import version
            dmc_version = version('dash-mantine-components')
            logger.info(f"Detected DMC version: {dmc_version}")
            return dmc_version
        except ImportError:
            logger.warning("dash-mantine-components not installed - using registry fallback")
            return None
        except Exception as e:
            logger.warning(f"Could not detect DMC version: {e}")
            return None

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
                (path / '.viz-platform').exists()
            ):
                logger.info(f"Found project directory from PWD: {path}")
                return path

        # Strategy 3: Check current working directory
        cwd = Path.cwd()
        if (cwd / '.git').exists() or (cwd / '.env').exists() or (cwd / '.viz-platform').exists():
            logger.info(f"Found project directory from cwd: {cwd}")
            return cwd

        logger.debug("Could not determine project directory")
        return None


def load_config() -> Dict[str, any]:
    """
    Convenience function to load configuration.

    Returns:
        Configuration dictionary
    """
    config = VizPlatformConfig()
    return config.load()


def check_dmc_version() -> Dict[str, any]:
    """
    Check DMC installation status for SessionStart hook.

    Returns:
        Dict with installation status and version info
    """
    config = load_config()

    if not config.get('dmc_available'):
        return {
            'installed': False,
            'message': 'dash-mantine-components not installed. Run: pip install dash-mantine-components'
        }

    version = config.get('dmc_version', 'unknown')

    # Check for registry compatibility
    registry_path = Path(__file__).parent.parent / 'registry'
    major_minor = '.'.join(version.split('.')[:2]) if version else None
    registry_file = registry_path / f'dmc_{major_minor.replace(".", "_")}.json' if major_minor else None

    if registry_file and registry_file.exists():
        return {
            'installed': True,
            'version': version,
            'registry_available': True,
            'message': f'DMC {version} ready with component registry'
        }
    else:
        return {
            'installed': True,
            'version': version,
            'registry_available': False,
            'message': f'DMC {version} installed but no matching registry. Validation may be limited.'
        }
