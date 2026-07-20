import asyncio
import psycopg
import polars as pl
from sqlalchemy import create_engine

from .base import RepositoryStore

class PostgresStore(RepositoryStore):
    def __init__(self, *, host: str, user: str, password: str, dbname: str, port: int | str):
        self._db_host = host
        self._db_user = user
        self._db_pass = password
        self._db_name = dbname
        self._db_port = port
        self._conn = psycopg.connect(
            dbname=self._db_name,
            user=self._db_user,
            password=self._db_pass,
            host=self._db_host,
            port=self._db_port,
        )
        self._compat_conn = create_engine(
            f"postgresql+psycopg://{self._db_user}:{self._db_pass}@{self._db_host}/{self._db_name}",
            echo=False,
            pool_pre_ping=True,
        )
        self._already_wrote = False

    async def write(self, data):
        if not self._already_wrote:
            await self._create_table()

        await asyncio.to_thread(
            data.write_database,
            table_name="repositories",
            connection=self._compat_conn,
            if_table_exists="append" if self._already_wrote else "replace",
        )

        if not self._already_wrote:
            self._already_wrote = True

        self._conn.commit()
    
    async def read(self, table, query = ""):
        return await asyncio.to_thread(
            pl.read_database,
            query=query if query is not None else f"SELECT * FROM {table}",
            connection=self._compat_conn,
        )
    
    async def _create_table(self) -> None:
        self._conn.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id BIGINT PRIMARY KEY,
            name TEXT,
            owner TEXT,
            stars INTEGER,
            forks INTEGER,
            watchers INTEGER,
            language TEXT,
            open_issues INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP         
        )
        """)