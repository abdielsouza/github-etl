import typer
import asyncio

from github_etl.pipeline import RepositoryPipeline
from github_etl.core.config import Config
from github_etl.discovery import *
from github_etl.extract.client import GithubClient
from github_etl.discovery.base import Discovery

app = typer.Typer()
config = Config.load("config/etl.toml")

async def scan_async():
    client = GithubClient()
    discoveries: list[Discovery] = [
        UserDiscovery(client, config.github.users),
        OrganizationDiscovery(client, config.github.orgs),
        RepositoryDiscovery(config.github.repos),
    ]

    results = await asyncio.gather(*(d.discover() for d in discoveries))
    repositories = [repo for repos in results for repo in repos]
    
    pipeline = RepositoryPipeline(
        client,
        repositories,
        config.database.path
    )
    
    await pipeline.run()

@app.command()
def scan():
    asyncio.run(scan_async())

if __name__ == '__main__':
    app()