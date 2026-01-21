"""
Configuration loader for Gitea MCP Server.

Implements hybrid configuration system:
- System-level: ~/.config/claude/gitea.env (credentials)
- Project-level: .env (repository specification)
- Auto-detection: Falls back to git remote URL parsing
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import re
import subprocess
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GiteaConfig:
    """Hybrid configuration loader with mode detection"""

    def __init__(self):
        self.api_url: Optional[str] = None
        self.api_token: Optional[str] = None
        self.repo: Optional[str] = None
        self.mode: str = 'project'

    def load(self) -> Dict[str, Optional[str]]:
        """
        Load configuration from system and project levels.
        Project-level configuration overrides system-level.

        Returns:
            Dict containing api_url, api_token, repo, mode

        Raises:
            FileNotFoundError: If system config is missing
            ValueError: If required configuration is missing
        """
        # Load system config
        system_config = Path.home() / '.config' / 'claude' / 'gitea.env'
        if system_config.exists():
            load_dotenv(system_config)
            logger.info(f"Loaded system configuration from {system_config}")
        else:
            raise FileNotFoundError(
                f"System config not found: {system_config}\n"
                "Create it with: mkdir -p ~/.config/claude && "
                "cat > ~/.config/claude/gitea.env"
            )

        # Load project config (overrides system)
        project_config = Path.cwd() / '.env'
        if project_config.exists():
            load_dotenv(project_config, override=True)
            logger.info(f"Loaded project configuration from {project_config}")

        # Extract values
        self.api_url = os.getenv('GITEA_API_URL')
        self.api_token = os.getenv('GITEA_API_TOKEN')
        self.repo = os.getenv('GITEA_REPO')  # Optional, must be owner/repo format

        # Auto-detect repo from git remote if not specified
        if not self.repo:
            self.repo = self._detect_repo_from_git()
            if self.repo:
                logger.info(f"Auto-detected repository from git remote: {self.repo}")

        # Detect mode
        if self.repo:
            self.mode = 'project'
            logger.info(f"Running in project mode: {self.repo}")
        else:
            self.mode = 'company'
            logger.info("Running in company-wide mode (PMO)")

        # Validate required variables
        self._validate()

        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'repo': self.repo,
            'mode': self.mode
        }

    def _validate(self) -> None:
        """
        Validate that required configuration is present.

        Raises:
            ValueError: If required configuration is missing
        """
        required = {
            'GITEA_API_URL': self.api_url,
            'GITEA_API_TOKEN': self.api_token
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Check your ~/.config/claude/gitea.env file"
            )

    def _detect_repo_from_git(self) -> Optional[str]:
        """
        Auto-detect repository from git remote origin URL.

        Supports URL formats:
        - SSH: ssh://git@host:port/owner/repo.git
        - SSH short: git@host:owner/repo.git
        - HTTPS: https://host/owner/repo.git
        - HTTP: http://host/owner/repo.git

        Returns:
            Repository in 'owner/repo' format, or None if detection fails
        """
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                logger.debug("No git remote 'origin' found")
                return None

            url = result.stdout.strip()
            return self._parse_git_url(url)

        except subprocess.TimeoutExpired:
            logger.warning("Git command timed out")
            return None
        except FileNotFoundError:
            logger.debug("Git not available")
            return None
        except Exception as e:
            logger.debug(f"Failed to detect repo from git: {e}")
            return None

    def _parse_git_url(self, url: str) -> Optional[str]:
        """
        Parse git URL to extract owner/repo.

        Args:
            url: Git remote URL

        Returns:
            Repository in 'owner/repo' format, or None if parsing fails
        """
        # Remove .git suffix if present
        url = re.sub(r'\.git$', '', url)

        # SSH format: ssh://git@host:port/owner/repo
        ssh_match = re.match(r'ssh://[^/]+/(.+/.+)$', url)
        if ssh_match:
            return ssh_match.group(1)

        # SSH short format: git@host:owner/repo
        ssh_short_match = re.match(r'git@[^:]+:(.+/.+)$', url)
        if ssh_short_match:
            return ssh_short_match.group(1)

        # HTTPS/HTTP format: https://host/owner/repo
        http_match = re.match(r'https?://[^/]+/(.+/.+)$', url)
        if http_match:
            return http_match.group(1)

        logger.warning(f"Could not parse git URL: {url}")
        return None
