import typer
import asyncio

from github_etl.pipeline import RepositoryPipeline
from github_etl.core.config import Config
from github_etl.discovery import *
from github_etl.utils import GithubClient

app = typer.Typer()
config = Config.load("config/etl.toml")

async def scan_async():
    client = GithubClient(token=config.github.token)
    
    pipeline = RepositoryPipeline(
        client,
        config.database.path
    )
    
    await pipeline.run()

@app.command()
def scan():
    asyncio.run(scan_async())

if __name__ == '__main__':
    app()