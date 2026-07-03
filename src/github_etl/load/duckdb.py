import duckdb

from github_etl.core.loader import Loader

class DuckDBLoader(Loader):
    def __init__(self, database: str):
        self._database = database

    def load(self, dataframe):
        conn = duckdb.connect(self._database)
        conn.execute("""
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
        conn.register("repos", dataframe)
        conn.execute("""
        INSERT INTO repositories
        SELECT * FROM repos
        """)
        conn.close()