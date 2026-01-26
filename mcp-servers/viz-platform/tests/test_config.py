"""
Unit tests for viz-platform configuration loader.
"""
import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def clean_env():
    """Clean environment variables before test"""
    env_vars = ['DMC_VERSION', 'CLAUDE_PROJECT_DIR', 'VIZ_DEFAULT_THEME']
    saved = {k: os.environ.get(k) for k in env_vars}
    for k in env_vars:
        if k in os.environ:
            del os.environ[k]
    yield
    # Restore after test
    for k, v in saved.items():
        if v is not None:
            os.environ[k] = v
        elif k in os.environ:
            del os.environ[k]


@pytest.fixture
def config():
    """Create VizPlatformConfig instance"""
    from mcp_server.config import VizPlatformConfig
    return VizPlatformConfig()


def test_config_init(config):
    """Test config initialization"""
    assert config.dmc_version is None
    assert config.theme_dir_user == Path.home() / '.config' / 'claude' / 'themes'
    assert config.theme_dir_project is None
    assert config.default_theme is None


def test_config_load_returns_dict(config, clean_env):
    """Test config.load() returns expected structure"""
    result = config.load()

    assert isinstance(result, dict)
    assert 'dmc_version' in result
    assert 'dmc_available' in result
    assert 'theme_dir_user' in result
    assert 'theme_dir_project' in result
    assert 'default_theme' in result
    assert 'project_dir' in result


def test_config_respects_env_dmc_version(config, clean_env):
    """Test that DMC_VERSION env var is respected"""
    os.environ['DMC_VERSION'] = '0.14.7'

    result = config.load()

    assert result['dmc_version'] == '0.14.7'
    assert result['dmc_available'] is True


def test_config_respects_default_theme_env(config, clean_env):
    """Test that VIZ_DEFAULT_THEME env var is respected"""
    os.environ['VIZ_DEFAULT_THEME'] = 'my-dark-theme'

    result = config.load()

    assert result['default_theme'] == 'my-dark-theme'


def test_detect_dmc_version_not_installed(config):
    """Test DMC version detection when not installed"""
    with patch('importlib.metadata.version', side_effect=ImportError("not installed")):
        version = config._detect_dmc_version()

    assert version is None


def test_detect_dmc_version_installed(config):
    """Test DMC version detection when installed"""
    with patch('importlib.metadata.version', return_value='0.14.7'):
        version = config._detect_dmc_version()

    assert version == '0.14.7'


def test_find_project_directory_from_env(config, clean_env, tmp_path):
    """Test project directory detection from CLAUDE_PROJECT_DIR"""
    os.environ['CLAUDE_PROJECT_DIR'] = str(tmp_path)

    result = config._find_project_directory()

    assert result == tmp_path


def test_find_project_directory_with_git(config, clean_env, tmp_path):
    """Test project directory detection with .git folder"""
    git_dir = tmp_path / '.git'
    git_dir.mkdir()

    with patch.dict(os.environ, {'PWD': str(tmp_path)}):
        result = config._find_project_directory()

    assert result == tmp_path


def test_find_project_directory_with_env_file(config, clean_env, tmp_path):
    """Test project directory detection with .env file"""
    env_file = tmp_path / '.env'
    env_file.touch()

    with patch.dict(os.environ, {'PWD': str(tmp_path)}):
        result = config._find_project_directory()

    assert result == tmp_path


def test_load_config_convenience_function(clean_env):
    """Test the convenience function load_config()"""
    from mcp_server.config import load_config

    result = load_config()

    assert isinstance(result, dict)
    assert 'dmc_version' in result


def test_check_dmc_version_not_installed(clean_env):
    """Test check_dmc_version when DMC not installed"""
    from mcp_server.config import check_dmc_version

    with patch('mcp_server.config.load_config', return_value={'dmc_available': False}):
        result = check_dmc_version()

    assert result['installed'] is False
    assert 'not installed' in result['message'].lower()


def test_check_dmc_version_installed_with_registry(clean_env, tmp_path):
    """Test check_dmc_version when DMC installed with matching registry"""
    from mcp_server.config import check_dmc_version

    mock_config = {
        'dmc_available': True,
        'dmc_version': '2.5.1'
    }

    with patch('mcp_server.config.load_config', return_value=mock_config):
        with patch('pathlib.Path.exists', return_value=True):
            result = check_dmc_version()

    assert result['installed'] is True
    assert result['version'] == '2.5.1'
