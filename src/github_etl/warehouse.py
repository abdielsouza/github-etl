from pathlib import Path
import duckdb

class Warehouse:
    def __init__(self, database: str):
        self._database = Path(database)
    
    @property
    def connection(self):
        return duckdb.connect(self._database)
    
    def query(self, sql: str):
        with self.connection as conn:
            return conn.sql(sql).pl()
    
    def execute(self, sql: str):
        with self.connection as conn:
            conn.execute(sql)