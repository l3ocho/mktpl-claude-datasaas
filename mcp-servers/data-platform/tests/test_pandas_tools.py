"""
Unit tests for pandas MCP tools.
"""
import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_csv(tmp_path):
    """Create a temporary CSV file for testing"""
    csv_path = tmp_path / 'test.csv'
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'value': [10.5, 20.0, 30.5, 40.0, 50.5]
    })
    df.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def temp_parquet(tmp_path):
    """Create a temporary Parquet file for testing"""
    parquet_path = tmp_path / 'test.parquet'
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'data': ['a', 'b', 'c']
    })
    df.to_parquet(parquet_path)
    return str(parquet_path)


@pytest.fixture
def temp_json(tmp_path):
    """Create a temporary JSON file for testing"""
    json_path = tmp_path / 'test.json'
    df = pd.DataFrame({
        'x': [1, 2],
        'y': [3, 4]
    })
    df.to_json(json_path, orient='records')
    return str(json_path)


@pytest.fixture
def pandas_tools():
    """Create PandasTools instance with fresh store"""
    from mcp_server.pandas_tools import PandasTools
    from mcp_server.data_store import DataStore

    # Reset store for test isolation
    store = DataStore.get_instance()
    store._dataframes = {}
    store._metadata = {}

    return PandasTools()


@pytest.mark.asyncio
async def test_read_csv(pandas_tools, temp_csv):
    """Test reading CSV file"""
    result = await pandas_tools.read_csv(temp_csv, name='csv_test')

    assert 'data_ref' in result
    assert result['data_ref'] == 'csv_test'
    assert result['rows'] == 5
    assert 'id' in result['columns']
    assert 'name' in result['columns']


@pytest.mark.asyncio
async def test_read_csv_nonexistent(pandas_tools):
    """Test reading nonexistent CSV file"""
    result = await pandas_tools.read_csv('/nonexistent/path.csv')

    assert 'error' in result
    assert 'not found' in result['error'].lower()


@pytest.mark.asyncio
async def test_read_parquet(pandas_tools, temp_parquet):
    """Test reading Parquet file"""
    result = await pandas_tools.read_parquet(temp_parquet, name='parquet_test')

    assert 'data_ref' in result
    assert result['rows'] == 3


@pytest.mark.asyncio
async def test_read_json(pandas_tools, temp_json):
    """Test reading JSON file"""
    result = await pandas_tools.read_json(temp_json, name='json_test')

    assert 'data_ref' in result
    assert result['rows'] == 2


@pytest.mark.asyncio
async def test_to_csv(pandas_tools, temp_csv, tmp_path):
    """Test exporting to CSV"""
    # First load some data
    await pandas_tools.read_csv(temp_csv, name='export_test')

    # Export to new file
    output_path = str(tmp_path / 'output.csv')
    result = await pandas_tools.to_csv('export_test', output_path)

    assert result['success'] is True
    assert os.path.exists(output_path)


@pytest.mark.asyncio
async def test_to_parquet(pandas_tools, temp_csv, tmp_path):
    """Test exporting to Parquet"""
    await pandas_tools.read_csv(temp_csv, name='parquet_export')

    output_path = str(tmp_path / 'output.parquet')
    result = await pandas_tools.to_parquet('parquet_export', output_path)

    assert result['success'] is True
    assert os.path.exists(output_path)


@pytest.mark.asyncio
async def test_describe(pandas_tools, temp_csv):
    """Test describe statistics"""
    await pandas_tools.read_csv(temp_csv, name='describe_test')

    result = await pandas_tools.describe('describe_test')

    assert 'data_ref' in result
    assert 'shape' in result
    assert result['shape']['rows'] == 5
    assert 'statistics' in result
    assert 'null_counts' in result


@pytest.mark.asyncio
async def test_head(pandas_tools, temp_csv):
    """Test getting first N rows"""
    await pandas_tools.read_csv(temp_csv, name='head_test')

    result = await pandas_tools.head('head_test', n=3)

    assert result['returned_rows'] == 3
    assert len(result['data']) == 3


@pytest.mark.asyncio
async def test_tail(pandas_tools, temp_csv):
    """Test getting last N rows"""
    await pandas_tools.read_csv(temp_csv, name='tail_test')

    result = await pandas_tools.tail('tail_test', n=2)

    assert result['returned_rows'] == 2


@pytest.mark.asyncio
async def test_filter(pandas_tools, temp_csv):
    """Test filtering rows"""
    await pandas_tools.read_csv(temp_csv, name='filter_test')

    result = await pandas_tools.filter('filter_test', 'value > 25')

    assert 'data_ref' in result
    assert result['rows'] == 3  # 30.5, 40.0, 50.5


@pytest.mark.asyncio
async def test_filter_invalid_condition(pandas_tools, temp_csv):
    """Test filter with invalid condition"""
    await pandas_tools.read_csv(temp_csv, name='filter_error')

    result = await pandas_tools.filter('filter_error', 'invalid_column > 0')

    assert 'error' in result


@pytest.mark.asyncio
async def test_select(pandas_tools, temp_csv):
    """Test selecting columns"""
    await pandas_tools.read_csv(temp_csv, name='select_test')

    result = await pandas_tools.select('select_test', ['id', 'name'])

    assert 'data_ref' in result
    assert result['columns'] == ['id', 'name']


@pytest.mark.asyncio
async def test_select_invalid_column(pandas_tools, temp_csv):
    """Test select with invalid column"""
    await pandas_tools.read_csv(temp_csv, name='select_error')

    result = await pandas_tools.select('select_error', ['id', 'nonexistent'])

    assert 'error' in result
    assert 'available_columns' in result


@pytest.mark.asyncio
async def test_groupby(pandas_tools, tmp_path):
    """Test groupby aggregation"""
    # Create test data with groups
    csv_path = tmp_path / 'groupby.csv'
    df = pd.DataFrame({
        'category': ['A', 'A', 'B', 'B'],
        'value': [10, 20, 30, 40]
    })
    df.to_csv(csv_path, index=False)

    await pandas_tools.read_csv(str(csv_path), name='groupby_test')

    result = await pandas_tools.groupby(
        'groupby_test',
        by='category',
        agg={'value': 'sum'}
    )

    assert 'data_ref' in result
    assert result['rows'] == 2  # Two groups: A, B


@pytest.mark.asyncio
async def test_join(pandas_tools, tmp_path):
    """Test joining DataFrames"""
    # Create left table
    left_path = tmp_path / 'left.csv'
    pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C']
    }).to_csv(left_path, index=False)

    # Create right table
    right_path = tmp_path / 'right.csv'
    pd.DataFrame({
        'id': [1, 2, 4],
        'value': [100, 200, 400]
    }).to_csv(right_path, index=False)

    await pandas_tools.read_csv(str(left_path), name='left')
    await pandas_tools.read_csv(str(right_path), name='right')

    result = await pandas_tools.join('left', 'right', on='id', how='inner')

    assert 'data_ref' in result
    assert result['rows'] == 2  # Only id 1 and 2 match


@pytest.mark.asyncio
async def test_list_data(pandas_tools, temp_csv):
    """Test listing all DataFrames"""
    await pandas_tools.read_csv(temp_csv, name='list_test1')
    await pandas_tools.read_csv(temp_csv, name='list_test2')

    result = await pandas_tools.list_data()

    assert result['count'] == 2
    refs = [df['ref'] for df in result['dataframes']]
    assert 'list_test1' in refs
    assert 'list_test2' in refs


@pytest.mark.asyncio
async def test_drop_data(pandas_tools, temp_csv):
    """Test dropping DataFrame"""
    await pandas_tools.read_csv(temp_csv, name='drop_test')

    result = await pandas_tools.drop_data('drop_test')

    assert result['success'] is True

    # Verify it's gone
    list_result = await pandas_tools.list_data()
    refs = [df['ref'] for df in list_result['dataframes']]
    assert 'drop_test' not in refs


@pytest.mark.asyncio
async def test_drop_nonexistent(pandas_tools):
    """Test dropping nonexistent DataFrame"""
    result = await pandas_tools.drop_data('nonexistent')

    assert 'error' in result


@pytest.mark.asyncio
async def test_operations_on_nonexistent(pandas_tools):
    """Test operations on nonexistent data_ref"""
    result = await pandas_tools.describe('nonexistent')
    assert 'error' in result

    result = await pandas_tools.head('nonexistent')
    assert 'error' in result

    result = await pandas_tools.filter('nonexistent', 'x > 0')
    assert 'error' in result
