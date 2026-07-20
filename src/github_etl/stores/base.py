from abc import ABC, abstractmethod
import polars as pl

class RepositoryStore(ABC):
    """Abstract class for external data storage."""
    
    @abstractmethod
    async def write(self, data: pl.DataFrame) -> None:
        ...
    
    @abstractmethod
    async def read(self, table: str, query: str = "") -> pl.DataFrame:
        ...