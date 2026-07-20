from .stores import RepositoryStore

class Warehouse:
    def __init__(self, store: RepositoryStore):
        self._store = store
    
    async def query(self, table: str, sql: str):
        return await self._store.read(table, sql)