from .base import Discovery
from github_etl.models import RepositoryReference
from github_etl.extract.client import GithubClient
import asyncio

class UserDiscovery(Discovery):
    def __init__(self, client: GithubClient, users: list[str]):
        self._client = client
        self._users = users

    async def discover(self):
        tasks = [
            asyncio.create_task(self._discover_user(user)) for user in self._users
        ]
        results = await asyncio.gather(*tasks)
        repositories: list[RepositoryReference] = []

        for repos in results:
            repositories.extend(repos)
        
        return repositories
    
    async def _discover_user(self, user: str) -> list[RepositoryReference]:
        repositories = []
        page = 1

        while True:
            repos = await self._client.get(
                f"/users/{user}/repos?per_page=100&page={page}"
            )

            if not repos:
                break

            for repo in repos:
                repositories.append(RepositoryReference(repo["owner"]["login"], repo["name"]))
            
            page += 1
        
        return repositories