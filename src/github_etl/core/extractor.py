from abc import ABC, abstractmethod
from typing import Any

class Extractor(ABC):
    @abstractmethod
    async def extract(self) -> list[Any]: ...