from aiostream import stream, async_

from github_etl.core.pipeline import Pipeline
from github_etl.core.reporters.console_reporter import ConsoleReporter
from github_etl.utils import GithubClient
from github_etl.stages import *
from github_etl.discovery import *

from .stores import RepositoryStore

class RepositoryPipeline(Pipeline):
    def __init__(
        self,
        client: GithubClient,
        db_strategy: RepositoryStore,
        *,
        users: list[str] = [],
        orgs: list[str] = [],
        repos: list[str] = []
    ):
        super().__init__()

        self._client = client
        self._users = users
        self._orgs = orgs
        self._repos = repos

        self.extractor = ExtractStage(client)
        self.transformer = TransformStage()
        self.loader = LoadStage(db_strategy)
    
    async def run(self):
        reporter = ConsoleReporter()

        reporter.start(metrics=self._metrics)
        
        reporter.print("discovering repos...")
        
        discoveries: list[Discovery] = [
            UserDiscovery(self._client, self._users),
            OrganizationDiscovery(self._client, self._orgs),
            RepositoryDiscovery(self._repos),
        ]

        streams = [d.discover() for d in discoveries]
        repos = stream.merge(*streams)

        repos = stream.map(
            repos,
            async_(lambda repo, *_: self.extractor.process(repo, self._metrics)),
            task_limit=64,
            ordered=False,
        )

        repos = stream.map(
            repos,
            async_(lambda repo, *_: self.transformer.process(repo, self._metrics)),
            task_limit=64,
            ordered=False,
        )

        await stream.action(
            repos,
            async_(lambda repo: self.loader.process(repo, self._metrics)),
            task_limit=8,
            ordered=False,
        )

        reporter.finish(metrics=self._metrics)
    
    async def _discover_repos(self):
        discoveries: list[Discovery] = [
            UserDiscovery(self._client, self._users),
            OrganizationDiscovery(self._client, self._orgs),
            RepositoryDiscovery(self._repos),
        ]

        for discovery in discoveries:
            async for repo in discovery.discover():
                yield repo