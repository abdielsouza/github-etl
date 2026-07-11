from abc import ABC, abstractmethod

class Loader[Input](ABC):
    @abstractmethod
    async def load(self, data: Input) -> None: ...