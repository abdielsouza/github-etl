from abc import ABC, abstractmethod
from github_etl.models import RepositoryReference

class Discovery(ABC):
    @abstractmethod
    async def discover(self) -> list[RepositoryReference]:
        ...