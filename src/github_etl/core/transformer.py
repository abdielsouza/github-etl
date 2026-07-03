from abc import ABC, abstractmethod
from typing import Any

import polars as pl

class Transformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> pl.DataFrame: ...