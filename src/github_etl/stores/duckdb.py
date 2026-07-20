from pathlib import Path
import duckdb
import polars as pl

from .base import RepositoryStore

class DuckDBStore(RepositoryStore):
    """storage implementation for DuckDB. Used in local tests and debug environment."""

    def __init__(self, database: Path):
        self._database = database
    
    async def write(self, data):
        with duckdb.connect(self._database) as conn:
            conn.register("repositories_df", data)
            conn.execute("""
            CREATE OR REPLACE TABLE repositories AS SELECT * FROM repositories_df
            """)
    
    async def read(self, table, query = ""):
        with duckdb.connect(self._database, read_only=True) as conn:
            if not query or query == "":
                return conn.sql(f"SELECT * FROM {table}").pl()
            
            return conn.sql(query).pl()
