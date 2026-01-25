"""
PostgreSQL/PostGIS MCP Tools.

Provides database operations with connection pooling and PostGIS support.
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
import json

from .data_store import DataStore
from .config import load_config

logger = logging.getLogger(__name__)

# Optional imports - gracefully handle missing dependencies
try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False
    logger.warning("asyncpg not available - PostgreSQL tools will be disabled")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class PostgresTools:
    """PostgreSQL/PostGIS database tools"""

    def __init__(self):
        self.store = DataStore.get_instance()
        self.config = load_config()
        self.pool: Optional[Any] = None
        self.max_rows = self.config.get('max_rows', 100_000)

    async def _get_pool(self):
        """Get or create connection pool"""
        if not ASYNCPG_AVAILABLE:
            raise RuntimeError("asyncpg not installed - run: pip install asyncpg")

        if self.pool is None:
            postgres_url = self.config.get('postgres_url')
            if not postgres_url:
                raise RuntimeError(
                    "PostgreSQL not configured. Set POSTGRES_URL in "
                    "~/.config/claude/postgres.env"
                )
            self.pool = await asyncpg.create_pool(postgres_url, min_size=1, max_size=5)
        return self.pool

    async def pg_connect(self) -> Dict:
        """
        Test PostgreSQL connection and return status.

        Returns:
            Dict with connection status, version, and database info
        """
        if not ASYNCPG_AVAILABLE:
            return {
                'connected': False,
                'error': 'asyncpg not installed',
                'suggestion': 'pip install asyncpg'
            }

        postgres_url = self.config.get('postgres_url')
        if not postgres_url:
            return {
                'connected': False,
                'error': 'POSTGRES_URL not configured',
                'suggestion': 'Create ~/.config/claude/postgres.env with POSTGRES_URL=postgresql://...'
            }

        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                version = await conn.fetchval('SELECT version()')
                db_name = await conn.fetchval('SELECT current_database()')
                user = await conn.fetchval('SELECT current_user')

                # Check for PostGIS
                postgis_version = None
                try:
                    postgis_version = await conn.fetchval('SELECT PostGIS_Version()')
                except Exception:
                    pass

                return {
                    'connected': True,
                    'database': db_name,
                    'user': user,
                    'version': version.split(',')[0] if version else 'Unknown',
                    'postgis_version': postgis_version,
                    'postgis_available': postgis_version is not None
                }

        except Exception as e:
            logger.error(f"pg_connect failed: {e}")
            return {
                'connected': False,
                'error': str(e)
            }

    async def pg_query(
        self,
        query: str,
        params: Optional[List] = None,
        name: Optional[str] = None
    ) -> Dict:
        """
        Execute SELECT query and return results as data_ref.

        Args:
            query: SQL SELECT query
            params: Query parameters (positional, use $1, $2, etc.)
            name: Optional name for result data_ref

        Returns:
            Dict with data_ref for results or error
        """
        if not PANDAS_AVAILABLE:
            return {'error': 'pandas not available'}

        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                if params:
                    rows = await conn.fetch(query, *params)
                else:
                    rows = await conn.fetch(query)

                if not rows:
                    return {
                        'data_ref': None,
                        'rows': 0,
                        'message': 'Query returned no results'
                    }

                # Convert to DataFrame
                df = pd.DataFrame([dict(r) for r in rows])

                # Check row limit
                check = self.store.check_row_limit(len(df))
                if check['exceeded']:
                    return {
                        'error': 'row_limit_exceeded',
                        **check,
                        'preview': df.head(100).to_dict(orient='records')
                    }

                # Store result
                data_ref = self.store.store(df, name=name, source=f"pg_query: {query[:100]}...")
                return {
                    'data_ref': data_ref,
                    'rows': len(df),
                    'columns': list(df.columns)
                }

        except Exception as e:
            logger.error(f"pg_query failed: {e}")
            return {'error': str(e)}

    async def pg_execute(
        self,
        query: str,
        params: Optional[List] = None
    ) -> Dict:
        """
        Execute INSERT/UPDATE/DELETE query.

        Args:
            query: SQL DML query
            params: Query parameters

        Returns:
            Dict with affected rows count
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                if params:
                    result = await conn.execute(query, *params)
                else:
                    result = await conn.execute(query)

                # Parse result (e.g., "INSERT 0 1" or "UPDATE 5")
                parts = result.split()
                affected = int(parts[-1]) if parts else 0

                return {
                    'success': True,
                    'command': parts[0] if parts else 'UNKNOWN',
                    'affected_rows': affected
                }

        except Exception as e:
            logger.error(f"pg_execute failed: {e}")
            return {'error': str(e)}

    async def pg_tables(self, schema: str = 'public') -> Dict:
        """
        List all tables in schema.

        Args:
            schema: Schema name (default: public)

        Returns:
            Dict with list of tables
        """
        query = """
            SELECT
                table_name,
                table_type,
                (SELECT count(*) FROM information_schema.columns c
                 WHERE c.table_schema = t.table_schema
                 AND c.table_name = t.table_name) as column_count
            FROM information_schema.tables t
            WHERE table_schema = $1
            ORDER BY table_name
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, schema)
                tables = [
                    {
                        'name': r['table_name'],
                        'type': r['table_type'],
                        'columns': r['column_count']
                    }
                    for r in rows
                ]
                return {
                    'schema': schema,
                    'count': len(tables),
                    'tables': tables
                }
        except Exception as e:
            logger.error(f"pg_tables failed: {e}")
            return {'error': str(e)}

    async def pg_columns(self, table: str, schema: str = 'public') -> Dict:
        """
        Get column information for a table.

        Args:
            table: Table name
            schema: Schema name (default: public)

        Returns:
            Dict with column details
        """
        query = """
            SELECT
                column_name,
                data_type,
                udt_name,
                is_nullable,
                column_default,
                character_maximum_length,
                numeric_precision
            FROM information_schema.columns
            WHERE table_schema = $1 AND table_name = $2
            ORDER BY ordinal_position
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, schema, table)
                columns = [
                    {
                        'name': r['column_name'],
                        'type': r['data_type'],
                        'udt': r['udt_name'],
                        'nullable': r['is_nullable'] == 'YES',
                        'default': r['column_default'],
                        'max_length': r['character_maximum_length'],
                        'precision': r['numeric_precision']
                    }
                    for r in rows
                ]
                return {
                    'table': f'{schema}.{table}',
                    'column_count': len(columns),
                    'columns': columns
                }
        except Exception as e:
            logger.error(f"pg_columns failed: {e}")
            return {'error': str(e)}

    async def pg_schemas(self) -> Dict:
        """
        List all schemas in database.

        Returns:
            Dict with list of schemas
        """
        query = """
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                rows = await conn.fetch(query)
                schemas = [r['schema_name'] for r in rows]
                return {
                    'count': len(schemas),
                    'schemas': schemas
                }
        except Exception as e:
            logger.error(f"pg_schemas failed: {e}")
            return {'error': str(e)}

    async def st_tables(self, schema: str = 'public') -> Dict:
        """
        List PostGIS-enabled tables.

        Args:
            schema: Schema name (default: public)

        Returns:
            Dict with list of tables with geometry columns
        """
        query = """
            SELECT
                f_table_name as table_name,
                f_geometry_column as geometry_column,
                type as geometry_type,
                srid,
                coord_dimension
            FROM geometry_columns
            WHERE f_table_schema = $1
            ORDER BY f_table_name
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, schema)
                tables = [
                    {
                        'table': r['table_name'],
                        'geometry_column': r['geometry_column'],
                        'geometry_type': r['geometry_type'],
                        'srid': r['srid'],
                        'dimensions': r['coord_dimension']
                    }
                    for r in rows
                ]
                return {
                    'schema': schema,
                    'count': len(tables),
                    'postgis_tables': tables
                }
        except Exception as e:
            if 'geometry_columns' in str(e):
                return {
                    'error': 'PostGIS not installed or extension not enabled',
                    'suggestion': 'Run: CREATE EXTENSION IF NOT EXISTS postgis;'
                }
            logger.error(f"st_tables failed: {e}")
            return {'error': str(e)}

    async def st_geometry_type(self, table: str, column: str, schema: str = 'public') -> Dict:
        """
        Get geometry type of a column.

        Args:
            table: Table name
            column: Geometry column name
            schema: Schema name

        Returns:
            Dict with geometry type information
        """
        query = f"""
            SELECT DISTINCT ST_GeometryType({column}) as geom_type
            FROM {schema}.{table}
            WHERE {column} IS NOT NULL
            LIMIT 10
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                rows = await conn.fetch(query)
                types = [r['geom_type'] for r in rows]
                return {
                    'table': f'{schema}.{table}',
                    'column': column,
                    'geometry_types': types
                }
        except Exception as e:
            logger.error(f"st_geometry_type failed: {e}")
            return {'error': str(e)}

    async def st_srid(self, table: str, column: str, schema: str = 'public') -> Dict:
        """
        Get SRID of geometry column.

        Args:
            table: Table name
            column: Geometry column name
            schema: Schema name

        Returns:
            Dict with SRID information
        """
        query = f"""
            SELECT DISTINCT ST_SRID({column}) as srid
            FROM {schema}.{table}
            WHERE {column} IS NOT NULL
            LIMIT 1
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(query)
                srid = row['srid'] if row else None

                # Get SRID description
                srid_info = None
                if srid:
                    srid_query = """
                        SELECT srtext, proj4text
                        FROM spatial_ref_sys
                        WHERE srid = $1
                    """
                    srid_row = await conn.fetchrow(srid_query, srid)
                    if srid_row:
                        srid_info = {
                            'description': srid_row['srtext'][:200] if srid_row['srtext'] else None,
                            'proj4': srid_row['proj4text']
                        }

                return {
                    'table': f'{schema}.{table}',
                    'column': column,
                    'srid': srid,
                    'info': srid_info
                }
        except Exception as e:
            logger.error(f"st_srid failed: {e}")
            return {'error': str(e)}

    async def st_extent(self, table: str, column: str, schema: str = 'public') -> Dict:
        """
        Get bounding box of all geometries.

        Args:
            table: Table name
            column: Geometry column name
            schema: Schema name

        Returns:
            Dict with bounding box coordinates
        """
        query = f"""
            SELECT
                ST_XMin(extent) as xmin,
                ST_YMin(extent) as ymin,
                ST_XMax(extent) as xmax,
                ST_YMax(extent) as ymax
            FROM (
                SELECT ST_Extent({column}) as extent
                FROM {schema}.{table}
            ) sub
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(query)
                if row and row['xmin'] is not None:
                    return {
                        'table': f'{schema}.{table}',
                        'column': column,
                        'bbox': {
                            'xmin': float(row['xmin']),
                            'ymin': float(row['ymin']),
                            'xmax': float(row['xmax']),
                            'ymax': float(row['ymax'])
                        }
                    }
                return {
                    'table': f'{schema}.{table}',
                    'column': column,
                    'bbox': None,
                    'message': 'No geometries found or all NULL'
                }
        except Exception as e:
            logger.error(f"st_extent failed: {e}")
            return {'error': str(e)}

    async def close(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None


def check_connection() -> None:
    """
    Check PostgreSQL connection for SessionStart hook.
    Prints warning to stderr if connection fails.
    """
    import sys

    config = load_config()
    if not config.get('postgres_url'):
        print(
            "[data-platform] PostgreSQL not configured (POSTGRES_URL not set)",
            file=sys.stderr
        )
        return

    async def test():
        try:
            if not ASYNCPG_AVAILABLE:
                print(
                    "[data-platform] asyncpg not installed - PostgreSQL tools unavailable",
                    file=sys.stderr
                )
                return

            conn = await asyncpg.connect(config['postgres_url'], timeout=5)
            await conn.close()
            print("[data-platform] PostgreSQL connection OK", file=sys.stderr)
        except Exception as e:
            print(
                f"[data-platform] PostgreSQL connection failed: {e}",
                file=sys.stderr
            )

    asyncio.run(test())
