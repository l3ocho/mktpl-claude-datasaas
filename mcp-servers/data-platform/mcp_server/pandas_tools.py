"""
pandas MCP Tools.

Provides DataFrame operations with Arrow IPC data_ref persistence.
"""
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from .data_store import DataStore
from .config import load_config

logger = logging.getLogger(__name__)


class PandasTools:
    """pandas data manipulation tools with data_ref persistence"""

    def __init__(self):
        self.store = DataStore.get_instance()
        config = load_config()
        self.max_rows = config.get('max_rows', 100_000)
        self.store.set_max_rows(self.max_rows)

    def _check_and_store(
        self,
        df: pd.DataFrame,
        name: Optional[str] = None,
        source: Optional[str] = None
    ) -> Dict:
        """Check row limit and store DataFrame if within limits"""
        check = self.store.check_row_limit(len(df))
        if check['exceeded']:
            return {
                'error': 'row_limit_exceeded',
                **check,
                'preview': df.head(100).to_dict(orient='records')
            }

        data_ref = self.store.store(df, name=name, source=source)
        return {
            'data_ref': data_ref,
            'rows': len(df),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
        }

    async def read_csv(
        self,
        file_path: str,
        name: Optional[str] = None,
        chunk_size: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """
        Load CSV file into DataFrame.

        Args:
            file_path: Path to CSV file
            name: Optional name for data_ref
            chunk_size: If provided, process in chunks
            **kwargs: Additional pandas read_csv arguments

        Returns:
            Dict with data_ref or error info
        """
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}

        try:
            if chunk_size:
                # Chunked processing - return iterator info
                chunks = []
                for i, chunk in enumerate(pd.read_csv(path, chunksize=chunk_size, **kwargs)):
                    chunk_ref = self.store.store(chunk, name=f"{name or 'chunk'}_{i}", source=file_path)
                    chunks.append({'ref': chunk_ref, 'rows': len(chunk)})
                return {
                    'chunked': True,
                    'chunks': chunks,
                    'total_chunks': len(chunks)
                }

            df = pd.read_csv(path, **kwargs)
            return self._check_and_store(df, name=name, source=file_path)

        except Exception as e:
            logger.error(f"read_csv failed: {e}")
            return {'error': str(e)}

    async def read_parquet(
        self,
        file_path: str,
        name: Optional[str] = None,
        columns: Optional[List[str]] = None
    ) -> Dict:
        """
        Load Parquet file into DataFrame.

        Args:
            file_path: Path to Parquet file
            name: Optional name for data_ref
            columns: Optional list of columns to load

        Returns:
            Dict with data_ref or error info
        """
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}

        try:
            table = pq.read_table(path, columns=columns)
            df = table.to_pandas()
            return self._check_and_store(df, name=name, source=file_path)

        except Exception as e:
            logger.error(f"read_parquet failed: {e}")
            return {'error': str(e)}

    async def read_json(
        self,
        file_path: str,
        name: Optional[str] = None,
        lines: bool = False,
        **kwargs
    ) -> Dict:
        """
        Load JSON/JSONL file into DataFrame.

        Args:
            file_path: Path to JSON file
            name: Optional name for data_ref
            lines: If True, read as JSON Lines format
            **kwargs: Additional pandas read_json arguments

        Returns:
            Dict with data_ref or error info
        """
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}

        try:
            df = pd.read_json(path, lines=lines, **kwargs)
            return self._check_and_store(df, name=name, source=file_path)

        except Exception as e:
            logger.error(f"read_json failed: {e}")
            return {'error': str(e)}

    async def to_csv(
        self,
        data_ref: str,
        file_path: str,
        index: bool = False,
        **kwargs
    ) -> Dict:
        """
        Export DataFrame to CSV file.

        Args:
            data_ref: Reference to stored DataFrame
            file_path: Output file path
            index: Whether to include index
            **kwargs: Additional pandas to_csv arguments

        Returns:
            Dict with success status
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            df.to_csv(file_path, index=index, **kwargs)
            return {
                'success': True,
                'file_path': file_path,
                'rows': len(df),
                'size_bytes': Path(file_path).stat().st_size
            }
        except Exception as e:
            logger.error(f"to_csv failed: {e}")
            return {'error': str(e)}

    async def to_parquet(
        self,
        data_ref: str,
        file_path: str,
        compression: str = 'snappy'
    ) -> Dict:
        """
        Export DataFrame to Parquet file.

        Args:
            data_ref: Reference to stored DataFrame
            file_path: Output file path
            compression: Compression codec

        Returns:
            Dict with success status
        """
        table = self.store.get(data_ref)
        if table is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            pq.write_table(table, file_path, compression=compression)
            return {
                'success': True,
                'file_path': file_path,
                'rows': table.num_rows,
                'size_bytes': Path(file_path).stat().st_size
            }
        except Exception as e:
            logger.error(f"to_parquet failed: {e}")
            return {'error': str(e)}

    async def describe(self, data_ref: str) -> Dict:
        """
        Get statistical summary of DataFrame.

        Args:
            data_ref: Reference to stored DataFrame

        Returns:
            Dict with statistical summary
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            desc = df.describe(include='all')
            info = self.store.get_info(data_ref)

            return {
                'data_ref': data_ref,
                'shape': {'rows': len(df), 'columns': len(df.columns)},
                'columns': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'memory_mb': info.memory_bytes / (1024 * 1024) if info else None,
                'null_counts': df.isnull().sum().to_dict(),
                'statistics': desc.to_dict()
            }
        except Exception as e:
            logger.error(f"describe failed: {e}")
            return {'error': str(e)}

    async def head(self, data_ref: str, n: int = 10) -> Dict:
        """
        Get first N rows of DataFrame.

        Args:
            data_ref: Reference to stored DataFrame
            n: Number of rows

        Returns:
            Dict with rows as records
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            head_df = df.head(n)
            return {
                'data_ref': data_ref,
                'total_rows': len(df),
                'returned_rows': len(head_df),
                'columns': list(df.columns),
                'data': head_df.to_dict(orient='records')
            }
        except Exception as e:
            logger.error(f"head failed: {e}")
            return {'error': str(e)}

    async def tail(self, data_ref: str, n: int = 10) -> Dict:
        """
        Get last N rows of DataFrame.

        Args:
            data_ref: Reference to stored DataFrame
            n: Number of rows

        Returns:
            Dict with rows as records
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            tail_df = df.tail(n)
            return {
                'data_ref': data_ref,
                'total_rows': len(df),
                'returned_rows': len(tail_df),
                'columns': list(df.columns),
                'data': tail_df.to_dict(orient='records')
            }
        except Exception as e:
            logger.error(f"tail failed: {e}")
            return {'error': str(e)}

    async def filter(
        self,
        data_ref: str,
        condition: str,
        name: Optional[str] = None
    ) -> Dict:
        """
        Filter DataFrame rows by condition.

        Args:
            data_ref: Reference to stored DataFrame
            condition: pandas query string (e.g., "age > 30 and city == 'NYC'")
            name: Optional name for result data_ref

        Returns:
            Dict with new data_ref for filtered result
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            filtered = df.query(condition)
            result_name = name or f"{data_ref}_filtered"
            return self._check_and_store(
                filtered,
                name=result_name,
                source=f"filter({data_ref}, '{condition}')"
            )
        except Exception as e:
            logger.error(f"filter failed: {e}")
            return {'error': str(e)}

    async def select(
        self,
        data_ref: str,
        columns: List[str],
        name: Optional[str] = None
    ) -> Dict:
        """
        Select specific columns from DataFrame.

        Args:
            data_ref: Reference to stored DataFrame
            columns: List of column names to select
            name: Optional name for result data_ref

        Returns:
            Dict with new data_ref for selected columns
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            # Validate columns exist
            missing = [c for c in columns if c not in df.columns]
            if missing:
                return {
                    'error': f'Columns not found: {missing}',
                    'available_columns': list(df.columns)
                }

            selected = df[columns]
            result_name = name or f"{data_ref}_select"
            return self._check_and_store(
                selected,
                name=result_name,
                source=f"select({data_ref}, {columns})"
            )
        except Exception as e:
            logger.error(f"select failed: {e}")
            return {'error': str(e)}

    async def groupby(
        self,
        data_ref: str,
        by: Union[str, List[str]],
        agg: Dict[str, Union[str, List[str]]],
        name: Optional[str] = None
    ) -> Dict:
        """
        Group DataFrame and aggregate.

        Args:
            data_ref: Reference to stored DataFrame
            by: Column(s) to group by
            agg: Aggregation dict (e.g., {"sales": "sum", "count": "mean"})
            name: Optional name for result data_ref

        Returns:
            Dict with new data_ref for aggregated result
        """
        df = self.store.get_pandas(data_ref)
        if df is None:
            return {'error': f'DataFrame not found: {data_ref}'}

        try:
            grouped = df.groupby(by).agg(agg).reset_index()
            # Flatten column names if multi-level
            if isinstance(grouped.columns, pd.MultiIndex):
                grouped.columns = ['_'.join(col).strip('_') for col in grouped.columns]

            result_name = name or f"{data_ref}_grouped"
            return self._check_and_store(
                grouped,
                name=result_name,
                source=f"groupby({data_ref}, by={by})"
            )
        except Exception as e:
            logger.error(f"groupby failed: {e}")
            return {'error': str(e)}

    async def join(
        self,
        left_ref: str,
        right_ref: str,
        on: Optional[Union[str, List[str]]] = None,
        left_on: Optional[Union[str, List[str]]] = None,
        right_on: Optional[Union[str, List[str]]] = None,
        how: str = 'inner',
        name: Optional[str] = None
    ) -> Dict:
        """
        Join two DataFrames.

        Args:
            left_ref: Reference to left DataFrame
            right_ref: Reference to right DataFrame
            on: Column(s) to join on (if same name in both)
            left_on: Left join column(s)
            right_on: Right join column(s)
            how: Join type ('inner', 'left', 'right', 'outer')
            name: Optional name for result data_ref

        Returns:
            Dict with new data_ref for joined result
        """
        left_df = self.store.get_pandas(left_ref)
        right_df = self.store.get_pandas(right_ref)

        if left_df is None:
            return {'error': f'DataFrame not found: {left_ref}'}
        if right_df is None:
            return {'error': f'DataFrame not found: {right_ref}'}

        try:
            joined = pd.merge(
                left_df, right_df,
                on=on, left_on=left_on, right_on=right_on,
                how=how
            )
            result_name = name or f"{left_ref}_{right_ref}_joined"
            return self._check_and_store(
                joined,
                name=result_name,
                source=f"join({left_ref}, {right_ref}, how={how})"
            )
        except Exception as e:
            logger.error(f"join failed: {e}")
            return {'error': str(e)}

    async def list_data(self) -> Dict:
        """
        List all stored DataFrames.

        Returns:
            Dict with list of stored DataFrames and their info
        """
        refs = self.store.list_refs()
        return {
            'count': len(refs),
            'total_memory_mb': self.store.total_memory_mb(),
            'max_rows_limit': self.max_rows,
            'dataframes': refs
        }

    async def drop_data(self, data_ref: str) -> Dict:
        """
        Remove a DataFrame from storage.

        Args:
            data_ref: Reference to drop

        Returns:
            Dict with success status
        """
        if self.store.drop(data_ref):
            return {'success': True, 'dropped': data_ref}
        return {'error': f'DataFrame not found: {data_ref}'}
