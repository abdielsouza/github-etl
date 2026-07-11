from typing import AsyncIterator

from .base import Discovery
from github_etl.models import RepositoryReference
from github_etl.utils import GithubClient

class UserDiscovery(Discovery):
    def __init__(self, client: GithubClient, users: list[str]):
        self._client = client
        self._users = users

    async def discover(self) -> AsyncIterator[RepositoryReference]:
        print("user discover")
        for user in self._users:
            page = 1

            while True:
                try:
                    data = await self._client.get(f"/users/{user}/repos?per_page=100&page={page}")

                    if not data:
                        break

                    for repo in data:
                        yield RepositoryReference(repo["owner"]["login"], repo["name"])
                    
                    page += 1
                
                except Exception as e:
                    raise e