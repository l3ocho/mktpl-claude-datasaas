"""
Configuration loader for NetBox MCP Server.

Implements hybrid configuration system:
- System-level: ~/.config/claude/netbox.env (credentials)
- Project-level: .env (optional overrides)
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from typing import Dict, List, Optional, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# All available NetBox modules
ALL_MODULES = frozenset([
    'dcim', 'ipam', 'circuits', 'virtualization',
    'tenancy', 'vpn', 'wireless', 'extras'
])


class NetBoxConfig:
    """Configuration loader for NetBox MCP Server"""

    def __init__(self):
        self.api_url: Optional[str] = None
        self.api_token: Optional[str] = None
        self.verify_ssl: bool = True
        self.timeout: int = 30
        self.enabled_modules: Set[str] = set(ALL_MODULES)

    def load(self) -> Dict[str, any]:
        """
        Load configuration from system and project levels.
        Project-level configuration overrides system-level.

        Returns:
            Dict containing api_url, api_token, verify_ssl, timeout

        Raises:
            FileNotFoundError: If system config is missing
            ValueError: If required configuration is missing
        """
        # Load system config
        system_config = Path.home() / '.config' / 'claude' / 'netbox.env'
        if system_config.exists():
            load_dotenv(system_config)
            logger.info(f"Loaded system configuration from {system_config}")
        else:
            raise FileNotFoundError(
                f"System config not found: {system_config}\n"
                "Create it with:\n"
                "  mkdir -p ~/.config/claude\n"
                "  cat > ~/.config/claude/netbox.env << EOF\n"
                "  NETBOX_API_URL=https://your-netbox-instance/api\n"
                "  NETBOX_API_TOKEN=your-api-token\n"
                "  EOF"
            )

        # Load project config (overrides system)
        project_config = Path.cwd() / '.env'
        if project_config.exists():
            load_dotenv(project_config, override=True)
            logger.info(f"Loaded project configuration from {project_config}")

        # Extract values
        self.api_url = os.getenv('NETBOX_API_URL')
        self.api_token = os.getenv('NETBOX_API_TOKEN')

        # Optional settings with defaults
        verify_ssl_str = os.getenv('NETBOX_VERIFY_SSL', 'true').lower()
        self.verify_ssl = verify_ssl_str in ('true', '1', 'yes')

        timeout_str = os.getenv('NETBOX_TIMEOUT', '30')
        try:
            self.timeout = int(timeout_str)
        except ValueError:
            self.timeout = 30
            logger.warning(f"Invalid NETBOX_TIMEOUT value '{timeout_str}', using default 30")

        # Module filtering
        self.enabled_modules = self._load_enabled_modules()

        # Validate required variables
        self._validate()

        # Normalize API URL (remove trailing slash)
        if self.api_url and self.api_url.endswith('/'):
            self.api_url = self.api_url.rstrip('/')

        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'verify_ssl': self.verify_ssl,
            'timeout': self.timeout,
            'enabled_modules': self.enabled_modules
        }

    def _validate(self) -> None:
        """
        Validate that required configuration is present.

        Raises:
            ValueError: If required configuration is missing
        """
        required = {
            'NETBOX_API_URL': self.api_url,
            'NETBOX_API_TOKEN': self.api_token
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Check your ~/.config/claude/netbox.env file"
            )

    def _load_enabled_modules(self) -> Set[str]:
        """
        Load enabled modules from NETBOX_ENABLED_MODULES environment variable.

        Format: Comma-separated list of module names.
        Example: NETBOX_ENABLED_MODULES=dcim,ipam,virtualization,extras

        Returns:
            Set of enabled module names. If env var is unset/empty, returns all modules.
        """
        modules_str = os.getenv('NETBOX_ENABLED_MODULES', '').strip()

        if not modules_str:
            logger.info("NETBOX_ENABLED_MODULES not set, all modules enabled (default)")
            return set(ALL_MODULES)

        # Parse comma-separated list, strip whitespace
        requested = {m.strip().lower() for m in modules_str.split(',') if m.strip()}

        # Validate module names
        invalid = requested - ALL_MODULES
        if invalid:
            logger.warning(
                f"Unknown modules in NETBOX_ENABLED_MODULES: {', '.join(sorted(invalid))}. "
                f"Valid modules: {', '.join(sorted(ALL_MODULES))}"
            )

        # Return only valid modules
        enabled = requested & ALL_MODULES

        if not enabled:
            logger.warning("No valid modules enabled, falling back to all modules")
            return set(ALL_MODULES)

        logger.info(f"Enabled modules: {', '.join(sorted(enabled))}")
        return enabled
