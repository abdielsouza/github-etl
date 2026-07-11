from typing import AsyncIterator

from .base import Discovery
from github_etl.models import RepositoryReference
from github_etl.utils import GithubClient

class OrganizationDiscovery(Discovery):
    def __init__(self, client: GithubClient, orgs: list[str]):
        self._client = client
        self._orgs = orgs

    async def discover(self) -> AsyncIterator[RepositoryReference]:
        print("org discovery")
        for org in self._orgs:
            page = 1

            while True:
                data = await self._client.get(f"/orgs/{org}/repos?per_page=100&page={page}")

                if not data:
                    break

                for repo in data:
                    yield RepositoryReference(repo["owner"]["login"], repo["name"])