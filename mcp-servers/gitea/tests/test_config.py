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


# ========================================
# GIT URL PARSING TESTS
# ========================================

def test_parse_git_url_ssh_format():
    """Test parsing SSH format git URL"""
    config = GiteaConfig()

    # SSH with port: ssh://git@host:port/owner/repo.git
    url = "ssh://git@hotserv.tailc9b278.ts.net:2222/personal-projects/personal-portfolio.git"
    result = config._parse_git_url(url)
    assert result == "personal-projects/personal-portfolio"


def test_parse_git_url_ssh_short_format():
    """Test parsing SSH short format git URL"""
    config = GiteaConfig()

    # SSH short: git@host:owner/repo.git
    url = "git@github.com:owner/repo.git"
    result = config._parse_git_url(url)
    assert result == "owner/repo"


def test_parse_git_url_https_format():
    """Test parsing HTTPS format git URL"""
    config = GiteaConfig()

    # HTTPS: https://host/owner/repo.git
    url = "https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace.git"
    result = config._parse_git_url(url)
    assert result == "personal-projects/leo-claude-mktplace"


def test_parse_git_url_http_format():
    """Test parsing HTTP format git URL"""
    config = GiteaConfig()

    # HTTP: http://host/owner/repo.git
    url = "http://gitea.hotserv.cloud/personal-projects/repo.git"
    result = config._parse_git_url(url)
    assert result == "personal-projects/repo"


def test_parse_git_url_without_git_suffix():
    """Test parsing git URL without .git suffix"""
    config = GiteaConfig()

    url = "https://github.com/owner/repo"
    result = config._parse_git_url(url)
    assert result == "owner/repo"


def test_parse_git_url_invalid_format():
    """Test parsing invalid git URL returns None"""
    config = GiteaConfig()

    url = "not-a-valid-url"
    result = config._parse_git_url(url)
    assert result is None


def test_find_project_directory_from_env(tmp_path, monkeypatch):
    """Test finding project directory from CLAUDE_PROJECT_DIR env var"""
    project_dir = tmp_path / 'my-project'
    project_dir.mkdir()
    (project_dir / '.git').mkdir()

    monkeypatch.setenv('CLAUDE_PROJECT_DIR', str(project_dir))

    config = GiteaConfig()
    result = config._find_project_directory()

    assert result == project_dir


def test_find_project_directory_from_cwd(tmp_path, monkeypatch):
    """Test finding project directory from cwd with .env file"""
    project_dir = tmp_path / 'project'
    project_dir.mkdir()
    (project_dir / '.env').write_text("GITEA_REPO=test/repo")

    monkeypatch.chdir(project_dir)
    # Clear env vars that might interfere
    monkeypatch.delenv('CLAUDE_PROJECT_DIR', raising=False)
    monkeypatch.delenv('PWD', raising=False)

    config = GiteaConfig()
    result = config._find_project_directory()

    assert result == project_dir


def test_find_project_directory_none_when_no_markers(tmp_path, monkeypatch):
    """Test returns None when no project markers found"""
    empty_dir = tmp_path / 'empty'
    empty_dir.mkdir()

    monkeypatch.chdir(empty_dir)
    monkeypatch.delenv('CLAUDE_PROJECT_DIR', raising=False)
    monkeypatch.delenv('PWD', raising=False)
    monkeypatch.delenv('GITEA_REPO', raising=False)

    config = GiteaConfig()
    result = config._find_project_directory()

    assert result is None
