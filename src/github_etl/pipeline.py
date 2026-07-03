from github_etl.extract.repositories import RepositoryExtractor
from github_etl.transform.repositories import RepositoryTransformer
from github_etl.load.duckdb import DuckDBLoader
from github_etl.core.pipeline import Pipeline
from github_etl.models import RepositoryReference
from github_etl.extract.client import GithubClient

class RepositoryPipeline(Pipeline):
    def __init__(self, client: GithubClient, repositories: list[RepositoryReference], database: str):
        self.extractor = RepositoryExtractor(client, repositories)
        self.transformer = RepositoryTransformer()
        self.loader = DuckDBLoader(database)