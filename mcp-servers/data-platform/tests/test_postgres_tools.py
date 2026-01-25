"""
Unit tests for PostgreSQL MCP tools.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import pandas as pd


@pytest.fixture
def mock_config():
    """Mock configuration"""
    return {
        'postgres_url': 'postgresql://test:test@localhost:5432/testdb',
        'max_rows': 100000
    }


@pytest.fixture
def postgres_tools(mock_config):
    """Create PostgresTools instance with mocked config"""
    with patch('mcp_server.postgres_tools.load_config', return_value=mock_config):
        from mcp_server.postgres_tools import PostgresTools
        from mcp_server.data_store import DataStore

        # Reset store
        store = DataStore.get_instance()
        store._dataframes = {}
        store._metadata = {}

        tools = PostgresTools()
        tools.config = mock_config
        return tools


@pytest.mark.asyncio
async def test_pg_connect_no_config():
    """Test pg_connect when no PostgreSQL configured"""
    with patch('mcp_server.postgres_tools.load_config', return_value={'postgres_url': None}):
        from mcp_server.postgres_tools import PostgresTools

        tools = PostgresTools()
        tools.config = {'postgres_url': None}

        result = await tools.pg_connect()

        assert result['connected'] is False
        assert 'not configured' in result['error'].lower()


@pytest.mark.asyncio
async def test_pg_connect_success(postgres_tools):
    """Test successful pg_connect"""
    mock_conn = AsyncMock()
    mock_conn.fetchval = AsyncMock(side_effect=[
        'PostgreSQL 15.1',  # version
        'testdb',           # database name
        'testuser',         # user
        None                # PostGIS check fails
    ])
    mock_conn.close = AsyncMock()

    # Create proper async context manager
    mock_cm = AsyncMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    mock_pool = MagicMock()
    mock_pool.acquire = MagicMock(return_value=mock_cm)

    # Use AsyncMock for create_pool since it's awaited
    with patch('asyncpg.create_pool', new=AsyncMock(return_value=mock_pool)):
        postgres_tools.pool = None
        result = await postgres_tools.pg_connect()

    assert result['connected'] is True
    assert result['database'] == 'testdb'


@pytest.mark.asyncio
async def test_pg_query_success(postgres_tools):
    """Test successful pg_query"""
    mock_rows = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]

    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=mock_rows)

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_query('SELECT * FROM users', name='users_data')

    assert 'data_ref' in result
    assert result['rows'] == 2


@pytest.mark.asyncio
async def test_pg_query_empty_result(postgres_tools):
    """Test pg_query with no results"""
    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=[])

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_query('SELECT * FROM empty_table')

    assert result['data_ref'] is None
    assert result['rows'] == 0


@pytest.mark.asyncio
async def test_pg_execute_success(postgres_tools):
    """Test successful pg_execute"""
    mock_conn = AsyncMock()
    mock_conn.execute = AsyncMock(return_value='INSERT 0 3')

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_execute('INSERT INTO users VALUES (1, 2, 3)')

    assert result['success'] is True
    assert result['affected_rows'] == 3
    assert result['command'] == 'INSERT'


@pytest.mark.asyncio
async def test_pg_tables(postgres_tools):
    """Test listing tables"""
    mock_rows = [
        {'table_name': 'users', 'table_type': 'BASE TABLE', 'column_count': 5},
        {'table_name': 'orders', 'table_type': 'BASE TABLE', 'column_count': 8}
    ]

    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=mock_rows)

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_tables(schema='public')

    assert result['schema'] == 'public'
    assert result['count'] == 2
    assert len(result['tables']) == 2


@pytest.mark.asyncio
async def test_pg_columns(postgres_tools):
    """Test getting column info"""
    mock_rows = [
        {
            'column_name': 'id',
            'data_type': 'integer',
            'udt_name': 'int4',
            'is_nullable': 'NO',
            'column_default': "nextval('users_id_seq'::regclass)",
            'character_maximum_length': None,
            'numeric_precision': 32
        },
        {
            'column_name': 'name',
            'data_type': 'character varying',
            'udt_name': 'varchar',
            'is_nullable': 'YES',
            'column_default': None,
            'character_maximum_length': 255,
            'numeric_precision': None
        }
    ]

    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=mock_rows)

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_columns(table='users')

    assert result['table'] == 'public.users'
    assert result['column_count'] == 2
    assert result['columns'][0]['name'] == 'id'
    assert result['columns'][0]['nullable'] is False


@pytest.mark.asyncio
async def test_pg_schemas(postgres_tools):
    """Test listing schemas"""
    mock_rows = [
        {'schema_name': 'public'},
        {'schema_name': 'app'}
    ]

    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=mock_rows)

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_schemas()

    assert result['count'] == 2
    assert 'public' in result['schemas']


@pytest.mark.asyncio
async def test_st_tables(postgres_tools):
    """Test listing PostGIS tables"""
    mock_rows = [
        {
            'table_name': 'locations',
            'geometry_column': 'geom',
            'geometry_type': 'POINT',
            'srid': 4326,
            'coord_dimension': 2
        }
    ]

    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(return_value=mock_rows)

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.st_tables()

    assert result['count'] == 1
    assert result['postgis_tables'][0]['table'] == 'locations'
    assert result['postgis_tables'][0]['srid'] == 4326


@pytest.mark.asyncio
async def test_st_tables_no_postgis(postgres_tools):
    """Test st_tables when PostGIS not installed"""
    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(side_effect=Exception("relation \"geometry_columns\" does not exist"))

    # Create proper async context manager
    mock_cm = AsyncMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    mock_pool = MagicMock()
    mock_pool.acquire = MagicMock(return_value=mock_cm)

    postgres_tools.pool = mock_pool

    result = await postgres_tools.st_tables()

    assert 'error' in result
    assert 'PostGIS' in result['error']


@pytest.mark.asyncio
async def test_st_extent(postgres_tools):
    """Test getting geometry bounding box"""
    mock_row = {
        'xmin': -122.5,
        'ymin': 37.5,
        'xmax': -122.0,
        'ymax': 38.0
    }

    mock_conn = AsyncMock()
    mock_conn.fetchrow = AsyncMock(return_value=mock_row)

    mock_pool = AsyncMock()
    mock_pool.acquire = MagicMock(return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=mock_conn),
        __aexit__=AsyncMock()
    ))

    postgres_tools.pool = mock_pool

    result = await postgres_tools.st_extent(table='locations', column='geom')

    assert result['bbox']['xmin'] == -122.5
    assert result['bbox']['ymax'] == 38.0


@pytest.mark.asyncio
async def test_error_handling(postgres_tools):
    """Test error handling for database errors"""
    mock_conn = AsyncMock()
    mock_conn.fetch = AsyncMock(side_effect=Exception("Connection refused"))

    # Create proper async context manager
    mock_cm = AsyncMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_cm.__aexit__ = AsyncMock(return_value=None)

    mock_pool = MagicMock()
    mock_pool.acquire = MagicMock(return_value=mock_cm)

    postgres_tools.pool = mock_pool

    result = await postgres_tools.pg_query('SELECT 1')

    assert 'error' in result
    assert 'Connection refused' in result['error']
