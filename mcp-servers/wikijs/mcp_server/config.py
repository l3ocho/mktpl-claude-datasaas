"""
Configuration loader for Wiki.js MCP Server.

Implements hybrid configuration system:
- System-level: ~/.config/claude/wikijs.env (credentials)
- Project-level: .env (project path specification)
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikiJSConfig:
    """Hybrid configuration loader with mode detection"""

    def __init__(self):
        self.api_url: Optional[str] = None
        self.api_token: Optional[str] = None
        self.base_path: Optional[str] = None
        self.project: Optional[str] = None
        self.mode: str = 'project'

    def load(self) -> Dict[str, Optional[str]]:
        """
        Load configuration from system and project levels.
        Project-level configuration overrides system-level.

        Returns:
            Dict containing api_url, api_token, base_path, project, mode

        Raises:
            FileNotFoundError: If system config is missing
            ValueError: If required configuration is missing
        """
        # Load system config
        system_config = Path.home() / '.config' / 'claude' / 'wikijs.env'
        if system_config.exists():
            load_dotenv(system_config)
            logger.info(f"Loaded system configuration from {system_config}")
        else:
            raise FileNotFoundError(
                f"System config not found: {system_config}\n"
                "Create it with: mkdir -p ~/.config/claude && "
                "cat > ~/.config/claude/wikijs.env"
            )

        # Load project config (overrides system)
        project_config = Path.cwd() / '.env'
        if project_config.exists():
            load_dotenv(project_config, override=True)
            logger.info(f"Loaded project configuration from {project_config}")

        # Extract values
        self.api_url = os.getenv('WIKIJS_API_URL')
        self.api_token = os.getenv('WIKIJS_API_TOKEN')
        self.base_path = os.getenv('WIKIJS_BASE_PATH')
        self.project = os.getenv('WIKIJS_PROJECT')  # Optional for PMO

        # Detect mode
        if self.project:
            self.mode = 'project'
            logger.info(f"Running in project mode: {self.project}")
        else:
            self.mode = 'company'
            logger.info("Running in company-wide mode (PMO)")

        # Validate required variables
        self._validate()

        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'base_path': self.base_path,
            'project': self.project,
            'mode': self.mode
        }

    def _validate(self) -> None:
        """
        Validate that required configuration is present.

        Raises:
            ValueError: If required configuration is missing
        """
        required = {
            'WIKIJS_API_URL': self.api_url,
            'WIKIJS_API_TOKEN': self.api_token,
            'WIKIJS_BASE_PATH': self.base_path
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Check your ~/.config/claude/wikijs.env file"
            )
