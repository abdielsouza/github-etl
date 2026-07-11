from abc import ABC, abstractmethod
from typing import AsyncIterator
from github_etl.models import RepositoryReference

class Discovery(ABC):
    @abstractmethod
    def discover(self) -> AsyncIterator[RepositoryReference]:
        ...