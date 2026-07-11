from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class RepositoryReference:
    owner: str
    name: str

    @property
    def full_name(self):
        return f"{self.owner}/{self.name}"

@dataclass(slots=True)
class QueueItem[T]:
    payload: Optional[T]
    stop: bool = False