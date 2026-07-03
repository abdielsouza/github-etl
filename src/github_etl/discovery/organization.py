from .base import Discovery
from github_etl.models import RepositoryReference
from github_etl.extract.client import GithubClient
import asyncio

class OrganizationDiscovery(Discovery):
    def __init__(self, client: GithubClient, orgs: list[str]):
        self._client = client
        self._orgs = orgs

    async def discover(self):
        tasks = [
            asyncio.create_task(self._discover_org(org)) for org in self._orgs
        ]
        results = await asyncio.gather(*tasks)
        repositories: list[RepositoryReference] = []

        for repos in results:
            repositories.extend(repos)
        
        return repositories
    
    async def _discover_org(self, org: str) -> list[RepositoryReference]:
        repositories = []
        page = 1

        while True:
            repos = await self._client.get(
                f"/orgs/{org}/repos?per_page=100&page={page}"
            )

            if not repos:
                break

            for repo in repos:
                repositories.append(RepositoryReference(repo["owner"]["login"], repo["name"]))
            
            page += 1
        
        return repositories