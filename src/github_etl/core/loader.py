from abc import ABC, abstractmethod
import polars as pl

class Loader(ABC):
    @abstractmethod
    def load(self, dataframe: pl.DataFrame) -> None: ...