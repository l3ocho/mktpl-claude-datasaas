"""
Arrow IPC DataFrame Registry.

Provides persistent storage for DataFrames across tool calls using Apache Arrow
for efficient memory management and serialization.
"""
import pyarrow as pa
import pandas as pd
import uuid
import logging
from typing import Dict, Optional, List, Union
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class DataFrameInfo:
    """Metadata about a stored DataFrame"""
    ref: str
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]
    memory_bytes: int
    created_at: datetime
    source: Optional[str] = None


class DataStore:
    """
    Singleton registry for Arrow Tables (DataFrames).

    Uses Arrow IPC format for efficient memory usage and supports
    data_ref based retrieval across multiple tool calls.
    """
    _instance = None
    _dataframes: Dict[str, pa.Table] = {}
    _metadata: Dict[str, DataFrameInfo] = {}
    _max_rows: int = 100_000

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._dataframes = {}
            cls._metadata = {}
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'DataStore':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def set_max_rows(cls, max_rows: int):
        """Set the maximum rows limit"""
        cls._max_rows = max_rows

    def store(
        self,
        data: Union[pa.Table, pd.DataFrame],
        name: Optional[str] = None,
        source: Optional[str] = None
    ) -> str:
        """
        Store a DataFrame and return its reference.

        Args:
            data: Arrow Table or pandas DataFrame
            name: Optional name for the reference (auto-generated if not provided)
            source: Optional source description (e.g., file path, query)

        Returns:
            data_ref string to retrieve the DataFrame later
        """
        # Convert pandas to Arrow if needed
        if isinstance(data, pd.DataFrame):
            table = pa.Table.from_pandas(data)
        else:
            table = data

        # Generate reference
        data_ref = name or f"df_{uuid.uuid4().hex[:8]}"

        # Ensure unique reference
        if data_ref in self._dataframes and name is None:
            data_ref = f"{data_ref}_{uuid.uuid4().hex[:4]}"

        # Store table
        self._dataframes[data_ref] = table

        # Store metadata
        schema = table.schema
        self._metadata[data_ref] = DataFrameInfo(
            ref=data_ref,
            rows=table.num_rows,
            columns=table.num_columns,
            column_names=[f.name for f in schema],
            dtypes={f.name: str(f.type) for f in schema},
            memory_bytes=table.nbytes,
            created_at=datetime.now(),
            source=source
        )

        logger.info(f"Stored DataFrame '{data_ref}': {table.num_rows} rows, {table.num_columns} cols")
        return data_ref

    def get(self, data_ref: str) -> Optional[pa.Table]:
        """
        Retrieve an Arrow Table by reference.

        Args:
            data_ref: Reference string from store()

        Returns:
            Arrow Table or None if not found
        """
        return self._dataframes.get(data_ref)

    def get_pandas(self, data_ref: str) -> Optional[pd.DataFrame]:
        """
        Retrieve a DataFrame as pandas.

        Args:
            data_ref: Reference string from store()

        Returns:
            pandas DataFrame or None if not found
        """
        table = self.get(data_ref)
        if table is not None:
            return table.to_pandas()
        return None

    def get_info(self, data_ref: str) -> Optional[DataFrameInfo]:
        """
        Get metadata about a stored DataFrame.

        Args:
            data_ref: Reference string

        Returns:
            DataFrameInfo or None if not found
        """
        return self._metadata.get(data_ref)

    def list_refs(self) -> List[Dict]:
        """
        List all stored DataFrame references with metadata.

        Returns:
            List of dicts with ref, rows, columns, memory info
        """
        result = []
        for ref, info in self._metadata.items():
            result.append({
                'ref': ref,
                'rows': info.rows,
                'columns': info.columns,
                'column_names': info.column_names,
                'memory_mb': round(info.memory_bytes / (1024 * 1024), 2),
                'source': info.source,
                'created_at': info.created_at.isoformat()
            })
        return result

    def drop(self, data_ref: str) -> bool:
        """
        Remove a DataFrame from the store.

        Args:
            data_ref: Reference string

        Returns:
            True if removed, False if not found
        """
        if data_ref in self._dataframes:
            del self._dataframes[data_ref]
            del self._metadata[data_ref]
            logger.info(f"Dropped DataFrame '{data_ref}'")
            return True
        return False

    def clear(self):
        """Remove all stored DataFrames"""
        count = len(self._dataframes)
        self._dataframes.clear()
        self._metadata.clear()
        logger.info(f"Cleared {count} DataFrames from store")

    def total_memory_bytes(self) -> int:
        """Get total memory used by all stored DataFrames"""
        return sum(info.memory_bytes for info in self._metadata.values())

    def total_memory_mb(self) -> float:
        """Get total memory in MB"""
        return round(self.total_memory_bytes() / (1024 * 1024), 2)

    def check_row_limit(self, row_count: int) -> Dict:
        """
        Check if row count exceeds limit.

        Args:
            row_count: Number of rows

        Returns:
            Dict with 'exceeded' bool and 'message' if exceeded
        """
        if row_count > self._max_rows:
            return {
                'exceeded': True,
                'message': f"Row count ({row_count:,}) exceeds limit ({self._max_rows:,})",
                'suggestion': f"Use chunked processing or filter data first",
                'limit': self._max_rows
            }
        return {'exceeded': False}
