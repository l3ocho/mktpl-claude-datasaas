"""
Unit tests for Arrow IPC DataFrame registry.
"""
import pytest
import pandas as pd
import pyarrow as pa


def test_store_pandas_dataframe():
    """Test storing pandas DataFrame"""
    from mcp_server.data_store import DataStore

    # Create fresh instance for test
    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    data_ref = store.store(df, name='test_df')

    assert data_ref == 'test_df'
    assert 'test_df' in store._dataframes
    assert store._metadata['test_df'].rows == 3
    assert store._metadata['test_df'].columns == 2


def test_store_arrow_table():
    """Test storing Arrow Table directly"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    table = pa.table({'x': [1, 2, 3], 'y': [4, 5, 6]})
    data_ref = store.store(table, name='arrow_test')

    assert data_ref == 'arrow_test'
    assert store._dataframes['arrow_test'].num_rows == 3


def test_store_auto_name():
    """Test auto-generated data_ref names"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    df = pd.DataFrame({'a': [1, 2]})
    data_ref = store.store(df)

    assert data_ref.startswith('df_')
    assert len(data_ref) == 11  # df_ + 8 hex chars


def test_get_dataframe():
    """Test retrieving stored DataFrame"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    df = pd.DataFrame({'a': [1, 2, 3]})
    store.store(df, name='get_test')

    result = store.get('get_test')
    assert result is not None
    assert result.num_rows == 3


def test_get_pandas():
    """Test retrieving as pandas DataFrame"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    store.store(df, name='pandas_test')

    result = store.get_pandas('pandas_test')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['a', 'b']
    assert len(result) == 3


def test_get_nonexistent():
    """Test getting nonexistent data_ref returns None"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    assert store.get('nonexistent') is None
    assert store.get_pandas('nonexistent') is None


def test_list_refs():
    """Test listing all stored DataFrames"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    store.store(pd.DataFrame({'a': [1, 2]}), name='df1')
    store.store(pd.DataFrame({'b': [3, 4, 5]}), name='df2')

    refs = store.list_refs()

    assert len(refs) == 2
    ref_names = [r['ref'] for r in refs]
    assert 'df1' in ref_names
    assert 'df2' in ref_names


def test_drop_dataframe():
    """Test dropping a DataFrame"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    store.store(pd.DataFrame({'a': [1]}), name='drop_test')
    assert store.get('drop_test') is not None

    result = store.drop('drop_test')
    assert result is True
    assert store.get('drop_test') is None


def test_drop_nonexistent():
    """Test dropping nonexistent data_ref"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    result = store.drop('nonexistent')
    assert result is False


def test_clear():
    """Test clearing all DataFrames"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    store.store(pd.DataFrame({'a': [1]}), name='df1')
    store.store(pd.DataFrame({'b': [2]}), name='df2')

    store.clear()

    assert len(store.list_refs()) == 0


def test_get_info():
    """Test getting DataFrame metadata"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    store.store(df, name='info_test', source='test source')

    info = store.get_info('info_test')

    assert info.ref == 'info_test'
    assert info.rows == 3
    assert info.columns == 2
    assert info.column_names == ['a', 'b']
    assert info.source == 'test source'
    assert info.memory_bytes > 0


def test_total_memory():
    """Test total memory calculation"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    store.store(pd.DataFrame({'a': range(100)}), name='df1')
    store.store(pd.DataFrame({'b': range(200)}), name='df2')

    total = store.total_memory_bytes()
    assert total > 0

    total_mb = store.total_memory_mb()
    assert total_mb >= 0


def test_check_row_limit():
    """Test row limit checking"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._max_rows = 100

    # Under limit
    result = store.check_row_limit(50)
    assert result['exceeded'] is False

    # Over limit
    result = store.check_row_limit(150)
    assert result['exceeded'] is True
    assert 'suggestion' in result


def test_metadata_dtypes():
    """Test that dtypes are correctly recorded"""
    from mcp_server.data_store import DataStore

    store = DataStore()
    store._dataframes = {}
    store._metadata = {}

    df = pd.DataFrame({
        'int_col': [1, 2, 3],
        'float_col': [1.1, 2.2, 3.3],
        'str_col': ['a', 'b', 'c']
    })
    store.store(df, name='dtype_test')

    info = store.get_info('dtype_test')

    assert 'int_col' in info.dtypes
    assert 'float_col' in info.dtypes
    assert 'str_col' in info.dtypes
