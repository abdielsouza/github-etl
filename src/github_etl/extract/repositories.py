from github_etl.core.extractor import Extractor
from github_etl.extract.client import GithubClient
from github_etl.models import RepositoryReference
import asyncio

class RepositoryExtractor(Extractor):
    def __init__(self, client: GithubClient, repositories: list[RepositoryReference]):
        self._client = client
        self._repositories = repositories
    
    async def extract(self):
        semaphore = asyncio.Semaphore(10)

        async def fetch(repo: RepositoryReference):
            async with semaphore:
                return await self._client.get(f"/repos/{repo.full_name}")
        
        tasks = [asyncio.create_task(fetch(repo)) for repo in self._repositories]

        return await asyncio.gather(*tasks)