from abc import ABC, abstractmethod

class Extractor[Input, Output](ABC):
    @abstractmethod
    async def extract(self, content: Input) -> Output: ...