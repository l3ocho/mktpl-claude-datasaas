"""
Unit tests for configuration loader.
"""
import pytest
from pathlib import Path
import os
from mcp_server.config import GiteaConfig


def test_load_system_config(tmp_path, monkeypatch):
    """Test loading system-level configuration"""
    # Mock home directory
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'gitea.env'
    config_file.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
    )

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    config = GiteaConfig()
    result = config.load()

    assert result['api_url'] == 'https://test.com/api/v1'
    assert result['api_token'] == 'test_token'
    assert result['owner'] == 'test_owner'
    assert result['mode'] == 'company'  # No repo specified
    assert result['repo'] is None


def test_project_config_override(tmp_path, monkeypatch):
    """Test that project config overrides system config"""
    # Set up system config
    system_config_dir = tmp_path / '.config' / 'claude'
    system_config_dir.mkdir(parents=True)

    system_config = system_config_dir / 'gitea.env'
    system_config.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
    )

    # Set up project config
    project_dir = tmp_path / 'project'
    project_dir.mkdir()

    project_config = project_dir / '.env'
    project_config.write_text("GITEA_REPO=test_repo\n")

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)

    config = GiteaConfig()
    result = config.load()

    assert result['repo'] == 'test_repo'
    assert result['mode'] == 'project'


def test_missing_system_config(tmp_path, monkeypatch):
    """Test error handling for missing system configuration"""
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError) as exc_info:
        config = GiteaConfig()
        config.load()

    assert "System config not found" in str(exc_info.value)


def test_missing_required_config(tmp_path, monkeypatch):
    """Test error handling for missing required variables"""
    # Clear environment variables
    for var in ['GITEA_API_URL', 'GITEA_API_TOKEN', 'GITEA_OWNER', 'GITEA_REPO']:
        monkeypatch.delenv(var, raising=False)

    # Create incomplete config
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'gitea.env'
    config_file.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        # Missing GITEA_API_TOKEN and GITEA_OWNER
    )

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError) as exc_info:
        config = GiteaConfig()
        config.load()

    assert "Missing required configuration" in str(exc_info.value)


def test_mode_detection_project(tmp_path, monkeypatch):
    """Test mode detection for project mode"""
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'gitea.env'
    config_file.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
        "GITEA_REPO=test_repo\n"
    )

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    config = GiteaConfig()
    result = config.load()

    assert result['mode'] == 'project'
    assert result['repo'] == 'test_repo'


def test_mode_detection_company(tmp_path, monkeypatch):
    """Test mode detection for company mode (PMO)"""
    # Clear environment variables, especially GITEA_REPO
    for var in ['GITEA_API_URL', 'GITEA_API_TOKEN', 'GITEA_OWNER', 'GITEA_REPO']:
        monkeypatch.delenv(var, raising=False)

    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'gitea.env'
    config_file.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
        # No GITEA_REPO
    )

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    config = GiteaConfig()
    result = config.load()

    assert result['mode'] == 'company'
    assert result['repo'] is None
