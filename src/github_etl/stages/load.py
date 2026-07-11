import duckdb
import polars as pl
from result import Ok, Err, Result

from .base import Stage

class LoadStage(Stage[Result[pl.DataFrame, Exception], None]):
    def __init__(self, database: str):
        self._database = database
        self._conn = duckdb.connect(self._database)
        self._conn.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id BIGINT,
            name VARCHAR,
            owner VARCHAR,
            stars INTEGER,
            forks INTEGER,
            watchers INTEGER,
            language VARCHAR,
            open_issues INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        """)

    async def process(self, item, metrics):
        try:
            if item.is_err():
                return Err(item.unwrap_err())
            
            df = item.unwrap()
            
            self._conn.register("repos", df)
            self._conn.execute("""
            INSERT INTO repositories
            SELECT * FROM repos
            """)
            metrics.loaded += 1

            return Ok(None)
        
        except Exception as e:
            metrics.failed += 1
            return Err(e)
    
    def close_connection(self):
        self._conn.close()
    
    def __delete__(self):
        self._conn.close()