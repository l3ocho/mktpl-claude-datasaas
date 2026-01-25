"""
Unit tests for configuration loader.
"""
import pytest
from pathlib import Path
import os


def test_load_system_config(tmp_path, monkeypatch):
    """Test loading system-level PostgreSQL configuration"""
    # Import here to avoid import errors before setup
    from mcp_server.config import DataPlatformConfig

    # Mock home directory
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'postgres.env'
    config_file.write_text(
        "POSTGRES_URL=postgresql://user:pass@localhost:5432/testdb\n"
    )

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    config = DataPlatformConfig()
    result = config.load()

    assert result['postgres_url'] == 'postgresql://user:pass@localhost:5432/testdb'
    assert result['postgres_available'] is True


def test_postgres_optional(tmp_path, monkeypatch):
    """Test that PostgreSQL configuration is optional"""
    from mcp_server.config import DataPlatformConfig

    # No postgres.env file
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    # Clear any existing env vars
    monkeypatch.delenv('POSTGRES_URL', raising=False)

    config = DataPlatformConfig()
    result = config.load()

    assert result['postgres_url'] is None
    assert result['postgres_available'] is False


def test_project_config_override(tmp_path, monkeypatch):
    """Test that project config overrides system config"""
    from mcp_server.config import DataPlatformConfig

    # Set up system config
    system_config_dir = tmp_path / '.config' / 'claude'
    system_config_dir.mkdir(parents=True)

    system_config = system_config_dir / 'postgres.env'
    system_config.write_text(
        "POSTGRES_URL=postgresql://system:pass@localhost:5432/systemdb\n"
    )

    # Set up project config
    project_dir = tmp_path / 'project'
    project_dir.mkdir()

    project_config = project_dir / '.env'
    project_config.write_text(
        "POSTGRES_URL=postgresql://project:pass@localhost:5432/projectdb\n"
        "DBT_PROJECT_DIR=/path/to/dbt\n"
    )

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)

    config = DataPlatformConfig()
    result = config.load()

    # Project config should override
    assert result['postgres_url'] == 'postgresql://project:pass@localhost:5432/projectdb'
    assert result['dbt_project_dir'] == '/path/to/dbt'


def test_max_rows_config(tmp_path, monkeypatch):
    """Test max rows configuration"""
    from mcp_server.config import DataPlatformConfig

    project_dir = tmp_path / 'project'
    project_dir.mkdir()

    project_config = project_dir / '.env'
    project_config.write_text("DATA_PLATFORM_MAX_ROWS=50000\n")

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)

    config = DataPlatformConfig()
    result = config.load()

    assert result['max_rows'] == 50000


def test_default_max_rows(tmp_path, monkeypatch):
    """Test default max rows value"""
    from mcp_server.config import DataPlatformConfig

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)

    # Clear any existing env vars
    monkeypatch.delenv('DATA_PLATFORM_MAX_ROWS', raising=False)

    config = DataPlatformConfig()
    result = config.load()

    assert result['max_rows'] == 100_000  # Default value


def test_dbt_auto_detection(tmp_path, monkeypatch):
    """Test automatic dbt project detection"""
    from mcp_server.config import DataPlatformConfig

    # Create project with dbt_project.yml
    project_dir = tmp_path / 'project'
    project_dir.mkdir()
    (project_dir / 'dbt_project.yml').write_text("name: test_project\n")

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)
    # Clear PWD and DBT_PROJECT_DIR to ensure auto-detection
    monkeypatch.delenv('PWD', raising=False)
    monkeypatch.delenv('DBT_PROJECT_DIR', raising=False)
    monkeypatch.delenv('CLAUDE_PROJECT_DIR', raising=False)

    config = DataPlatformConfig()
    result = config.load()

    assert result['dbt_project_dir'] == str(project_dir)
    assert result['dbt_available'] is True


def test_dbt_subdirectory_detection(tmp_path, monkeypatch):
    """Test dbt project detection in subdirectory"""
    from mcp_server.config import DataPlatformConfig

    # Create project with dbt in subdirectory
    project_dir = tmp_path / 'project'
    project_dir.mkdir()
    # Need a marker file for _find_project_directory to find the project
    (project_dir / '.git').mkdir()
    dbt_dir = project_dir / 'transform'
    dbt_dir.mkdir()
    (dbt_dir / 'dbt_project.yml').write_text("name: test_project\n")

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)
    # Clear env vars to ensure auto-detection
    monkeypatch.delenv('PWD', raising=False)
    monkeypatch.delenv('DBT_PROJECT_DIR', raising=False)
    monkeypatch.delenv('CLAUDE_PROJECT_DIR', raising=False)

    config = DataPlatformConfig()
    result = config.load()

    assert result['dbt_project_dir'] == str(dbt_dir)
    assert result['dbt_available'] is True


def test_no_dbt_project(tmp_path, monkeypatch):
    """Test when no dbt project exists"""
    from mcp_server.config import DataPlatformConfig

    project_dir = tmp_path / 'project'
    project_dir.mkdir()

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)

    # Clear any existing env vars
    monkeypatch.delenv('DBT_PROJECT_DIR', raising=False)

    config = DataPlatformConfig()
    result = config.load()

    assert result['dbt_project_dir'] is None
    assert result['dbt_available'] is False


def test_find_project_directory_from_env(tmp_path, monkeypatch):
    """Test finding project directory from CLAUDE_PROJECT_DIR env var"""
    from mcp_server.config import DataPlatformConfig

    project_dir = tmp_path / 'my-project'
    project_dir.mkdir()
    (project_dir / '.git').mkdir()

    monkeypatch.setenv('CLAUDE_PROJECT_DIR', str(project_dir))

    config = DataPlatformConfig()
    result = config._find_project_directory()

    assert result == project_dir


def test_find_project_directory_from_cwd(tmp_path, monkeypatch):
    """Test finding project directory from cwd with .env file"""
    from mcp_server.config import DataPlatformConfig

    project_dir = tmp_path / 'project'
    project_dir.mkdir()
    (project_dir / '.env').write_text("TEST=value")

    monkeypatch.chdir(project_dir)
    monkeypatch.delenv('CLAUDE_PROJECT_DIR', raising=False)
    monkeypatch.delenv('PWD', raising=False)

    config = DataPlatformConfig()
    result = config._find_project_directory()

    assert result == project_dir


def test_find_project_directory_none_when_no_markers(tmp_path, monkeypatch):
    """Test returns None when no project markers found"""
    from mcp_server.config import DataPlatformConfig

    empty_dir = tmp_path / 'empty'
    empty_dir.mkdir()

    monkeypatch.chdir(empty_dir)
    monkeypatch.delenv('CLAUDE_PROJECT_DIR', raising=False)
    monkeypatch.delenv('PWD', raising=False)
    monkeypatch.delenv('DBT_PROJECT_DIR', raising=False)

    config = DataPlatformConfig()
    result = config._find_project_directory()

    assert result is None
