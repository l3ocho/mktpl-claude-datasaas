"""
Unit tests for dbt MCP tools.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess
import json
import tempfile
import os


@pytest.fixture
def mock_config(tmp_path):
    """Mock configuration with dbt project"""
    dbt_dir = tmp_path / 'dbt_project'
    dbt_dir.mkdir()
    (dbt_dir / 'dbt_project.yml').write_text('name: test_project\n')

    return {
        'dbt_project_dir': str(dbt_dir),
        'dbt_profiles_dir': str(tmp_path / '.dbt')
    }


@pytest.fixture
def dbt_tools(mock_config):
    """Create DbtTools instance with mocked config"""
    with patch('mcp_server.dbt_tools.load_config', return_value=mock_config):
        from mcp_server.dbt_tools import DbtTools

        tools = DbtTools()
        tools.project_dir = mock_config['dbt_project_dir']
        tools.profiles_dir = mock_config['dbt_profiles_dir']
        return tools


@pytest.mark.asyncio
async def test_dbt_parse_success(dbt_tools):
    """Test successful dbt parse"""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = 'Parsed successfully'
    mock_result.stderr = ''

    with patch('subprocess.run', return_value=mock_result):
        result = await dbt_tools.dbt_parse()

    assert result['valid'] is True


@pytest.mark.asyncio
async def test_dbt_parse_failure(dbt_tools):
    """Test dbt parse with errors"""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ''
    mock_result.stderr = 'Compilation error: deprecated syntax'

    with patch('subprocess.run', return_value=mock_result):
        result = await dbt_tools.dbt_parse()

    assert result['valid'] is False
    assert 'deprecated' in str(result.get('details', '')).lower() or len(result.get('errors', [])) > 0


@pytest.mark.asyncio
async def test_dbt_run_with_prevalidation(dbt_tools):
    """Test dbt run includes pre-validation"""
    # First call is parse, second is run
    mock_parse = MagicMock()
    mock_parse.returncode = 0
    mock_parse.stdout = 'OK'
    mock_parse.stderr = ''

    mock_run = MagicMock()
    mock_run.returncode = 0
    mock_run.stdout = 'Completed successfully'
    mock_run.stderr = ''

    with patch('subprocess.run', side_effect=[mock_parse, mock_run]):
        result = await dbt_tools.dbt_run()

    assert result['success'] is True


@pytest.mark.asyncio
async def test_dbt_run_fails_validation(dbt_tools):
    """Test dbt run fails if validation fails"""
    mock_parse = MagicMock()
    mock_parse.returncode = 1
    mock_parse.stdout = ''
    mock_parse.stderr = 'Parse error'

    with patch('subprocess.run', return_value=mock_parse):
        result = await dbt_tools.dbt_run()

    assert 'error' in result
    assert 'Pre-validation failed' in result['error']


@pytest.mark.asyncio
async def test_dbt_run_with_selection(dbt_tools):
    """Test dbt run with model selection"""
    mock_parse = MagicMock()
    mock_parse.returncode = 0
    mock_parse.stdout = 'OK'
    mock_parse.stderr = ''

    mock_run = MagicMock()
    mock_run.returncode = 0
    mock_run.stdout = 'Completed'
    mock_run.stderr = ''

    calls = []

    def track_calls(*args, **kwargs):
        calls.append(args[0] if args else kwargs.get('args', []))
        if len(calls) == 1:
            return mock_parse
        return mock_run

    with patch('subprocess.run', side_effect=track_calls):
        result = await dbt_tools.dbt_run(select='dim_customers')

    # Verify --select was passed
    assert any('--select' in str(call) for call in calls)


@pytest.mark.asyncio
async def test_dbt_test(dbt_tools):
    """Test dbt test"""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = 'All tests passed'
    mock_result.stderr = ''

    with patch('subprocess.run', return_value=mock_result):
        result = await dbt_tools.dbt_test()

    assert result['success'] is True


@pytest.mark.asyncio
async def test_dbt_build(dbt_tools):
    """Test dbt build with pre-validation"""
    mock_parse = MagicMock()
    mock_parse.returncode = 0
    mock_parse.stdout = 'OK'
    mock_parse.stderr = ''

    mock_build = MagicMock()
    mock_build.returncode = 0
    mock_build.stdout = 'Build complete'
    mock_build.stderr = ''

    with patch('subprocess.run', side_effect=[mock_parse, mock_build]):
        result = await dbt_tools.dbt_build()

    assert result['success'] is True


@pytest.mark.asyncio
async def test_dbt_compile(dbt_tools):
    """Test dbt compile"""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = 'Compiled'
    mock_result.stderr = ''

    with patch('subprocess.run', return_value=mock_result):
        result = await dbt_tools.dbt_compile()

    assert result['success'] is True


@pytest.mark.asyncio
async def test_dbt_ls(dbt_tools):
    """Test dbt ls"""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = 'dim_customers\ndim_products\nfct_orders\n'
    mock_result.stderr = ''

    with patch('subprocess.run', return_value=mock_result):
        result = await dbt_tools.dbt_ls()

    assert result['success'] is True
    assert result['count'] == 3
    assert 'dim_customers' in result['resources']


@pytest.mark.asyncio
async def test_dbt_docs_generate(dbt_tools, tmp_path):
    """Test dbt docs generate"""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = 'Done'
    mock_result.stderr = ''

    # Create fake target directory
    target_dir = tmp_path / 'dbt_project' / 'target'
    target_dir.mkdir(parents=True)
    (target_dir / 'catalog.json').write_text('{}')
    (target_dir / 'manifest.json').write_text('{}')

    dbt_tools.project_dir = str(tmp_path / 'dbt_project')

    with patch('subprocess.run', return_value=mock_result):
        result = await dbt_tools.dbt_docs_generate()

    assert result['success'] is True
    assert result['catalog_generated'] is True
    assert result['manifest_generated'] is True


@pytest.mark.asyncio
async def test_dbt_lineage(dbt_tools, tmp_path):
    """Test dbt lineage"""
    # Create manifest
    target_dir = tmp_path / 'dbt_project' / 'target'
    target_dir.mkdir(parents=True)

    manifest = {
        'nodes': {
            'model.test.dim_customers': {
                'name': 'dim_customers',
                'resource_type': 'model',
                'schema': 'public',
                'database': 'testdb',
                'description': 'Customer dimension',
                'tags': ['daily'],
                'config': {'materialized': 'table'},
                'depends_on': {
                    'nodes': ['model.test.stg_customers']
                }
            },
            'model.test.stg_customers': {
                'name': 'stg_customers',
                'resource_type': 'model',
                'depends_on': {'nodes': []}
            },
            'model.test.fct_orders': {
                'name': 'fct_orders',
                'resource_type': 'model',
                'depends_on': {
                    'nodes': ['model.test.dim_customers']
                }
            }
        }
    }
    (target_dir / 'manifest.json').write_text(json.dumps(manifest))

    dbt_tools.project_dir = str(tmp_path / 'dbt_project')

    result = await dbt_tools.dbt_lineage('dim_customers')

    assert result['model'] == 'dim_customers'
    assert 'model.test.stg_customers' in result['upstream']
    assert 'model.test.fct_orders' in result['downstream']


@pytest.mark.asyncio
async def test_dbt_lineage_model_not_found(dbt_tools, tmp_path):
    """Test dbt lineage with nonexistent model"""
    target_dir = tmp_path / 'dbt_project' / 'target'
    target_dir.mkdir(parents=True)

    manifest = {
        'nodes': {
            'model.test.dim_customers': {
                'name': 'dim_customers',
                'resource_type': 'model'
            }
        }
    }
    (target_dir / 'manifest.json').write_text(json.dumps(manifest))

    dbt_tools.project_dir = str(tmp_path / 'dbt_project')

    result = await dbt_tools.dbt_lineage('nonexistent_model')

    assert 'error' in result
    assert 'not found' in result['error'].lower()


@pytest.mark.asyncio
async def test_dbt_no_project():
    """Test dbt tools when no project configured"""
    with patch('mcp_server.dbt_tools.load_config', return_value={'dbt_project_dir': None}):
        from mcp_server.dbt_tools import DbtTools

        tools = DbtTools()
        tools.project_dir = None

        result = await tools.dbt_run()

    assert 'error' in result
    assert 'not found' in result['error'].lower()


@pytest.mark.asyncio
async def test_dbt_timeout(dbt_tools):
    """Test dbt command timeout handling"""
    with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('dbt', 300)):
        result = await dbt_tools.dbt_parse()

    assert 'error' in result
    assert 'timed out' in result['error'].lower()


@pytest.mark.asyncio
async def test_dbt_not_installed(dbt_tools):
    """Test handling when dbt is not installed"""
    with patch('subprocess.run', side_effect=FileNotFoundError()):
        result = await dbt_tools.dbt_parse()

    assert 'error' in result
    assert 'not found' in result['error'].lower()
