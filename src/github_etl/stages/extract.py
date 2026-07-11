from result import Ok, Err

from .base import Stage
from github_etl.models import RepositoryReference
from github_etl.utils import GithubClient

class ExtractStage(Stage[RepositoryReference, dict]):
    def __init__(self, client: GithubClient):
        self._client = client

    async def process(self, item, metrics):
        try:
            repo_data = await self._client.get(f"/repos/{item.full_name}")
            metrics.extracted += 1

            return Ok(repo_data)
        
        except Exception as e:
            metrics.failed += 1
            return Err(e)