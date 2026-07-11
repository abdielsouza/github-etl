from abc import ABC, abstractmethod

class Transformer[Input, Output](ABC):
    @abstractmethod
    async def transform(self, data: Input) -> Output: ...