from .base import Discovery
from github_etl.models import RepositoryReference

class RepositoryDiscovery(Discovery):
    def __init__(self, repos: list[str]):
        self._repos = repos

    async def discover(self):
        repos = []
        for repo in self._repos:
            owner, name = repo.split("/")
            repos.append(RepositoryReference(owner, name))
        
        return repos