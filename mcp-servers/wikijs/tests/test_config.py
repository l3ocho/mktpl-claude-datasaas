"""
Tests for WikiJS configuration loader.
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from mcp_server.config import WikiJSConfig


@pytest.fixture
def mock_env(monkeypatch, tmp_path):
    """Mock environment with temporary config files"""
    # Create mock system config
    system_config = tmp_path / ".config" / "claude" / "wikijs.env"
    system_config.parent.mkdir(parents=True)
    system_config.write_text(
        "WIKIJS_API_URL=http://wiki.test.com/graphql\n"
        "WIKIJS_API_TOKEN=test_token_123\n"
        "WIKIJS_BASE_PATH=/test-company\n"
    )

    # Mock Path.home()
    with patch('pathlib.Path.home', return_value=tmp_path):
        yield tmp_path


def test_load_system_config(mock_env):
    """Test loading system-level configuration"""
    config = WikiJSConfig()
    result = config.load()

    assert result['api_url'] == "http://wiki.test.com/graphql"
    assert result['api_token'] == "test_token_123"
    assert result['base_path'] == "/test-company"
    assert result['project'] is None
    assert result['mode'] == 'company'  # No project = company mode


def test_project_config_override(mock_env, tmp_path, monkeypatch):
    """Test project-level config overrides system-level"""
    # Create project-level config
    project_config = tmp_path / ".env"
    project_config.write_text(
        "WIKIJS_PROJECT=projects/test-project\n"
    )

    # Mock Path.cwd()
    monkeypatch.setattr('pathlib.Path.cwd', lambda: tmp_path)

    config = WikiJSConfig()
    result = config.load()

    assert result['api_url'] == "http://wiki.test.com/graphql"  # From system
    assert result['project'] == "projects/test-project"  # From project
    assert result['mode'] == 'project'  # Has project = project mode


def test_missing_system_config():
    """Test error when system config is missing"""
    with patch('pathlib.Path.home', return_value=Path('/nonexistent')):
        config = WikiJSConfig()
        with pytest.raises(FileNotFoundError, match="System config not found"):
            config.load()


def test_missing_required_config(mock_env, monkeypatch):
    """Test validation of required configuration"""
    # Clear environment variables from previous tests
    monkeypatch.delenv('WIKIJS_API_URL', raising=False)
    monkeypatch.delenv('WIKIJS_API_TOKEN', raising=False)
    monkeypatch.delenv('WIKIJS_BASE_PATH', raising=False)
    monkeypatch.delenv('WIKIJS_PROJECT', raising=False)

    # Create incomplete system config
    system_config = mock_env / ".config" / "claude" / "wikijs.env"
    system_config.write_text(
        "WIKIJS_API_URL=http://wiki.test.com/graphql\n"
        # Missing API_TOKEN and BASE_PATH
    )

    config = WikiJSConfig()
    with pytest.raises(ValueError, match="Missing required configuration"):
        config.load()


def test_mode_detection_project(mock_env, tmp_path, monkeypatch):
    """Test mode detection when WIKIJS_PROJECT is set"""
    project_config = tmp_path / ".env"
    project_config.write_text("WIKIJS_PROJECT=projects/my-project\n")

    monkeypatch.setattr('pathlib.Path.cwd', lambda: tmp_path)

    config = WikiJSConfig()
    result = config.load()

    assert result['mode'] == 'project'
    assert result['project'] == 'projects/my-project'


def test_mode_detection_company(mock_env, monkeypatch):
    """Test mode detection when WIKIJS_PROJECT is not set (company mode)"""
    # Clear WIKIJS_PROJECT from environment
    monkeypatch.delenv('WIKIJS_PROJECT', raising=False)

    config = WikiJSConfig()
    result = config.load()

    assert result['mode'] == 'company'
    assert result['project'] is None
