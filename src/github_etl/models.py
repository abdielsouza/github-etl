from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RepositoryReference:
    owner: str
    name: str

    @property
    def full_name(self):
        return f"{self.owner}/{self.name}"

@dataclass(slots=True, frozen=True)
class RepositoryData:
    id:             str
    name:           str
    owner:          str
    stars:          int
    forks:          int
    watchers:       int
    language:       str
    open_issues:    int
    created_at:     datetime
    updated_at:     datetime