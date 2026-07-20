import typer
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from github_etl.pipeline import RepositoryPipeline
from github_etl.core.config import Config
from github_etl.discovery import *
from github_etl.utils import GithubClient

from .stores import DuckDBStore, PostgresStore

app = typer.Typer()

TEST_DISCOVERY_INFO = {
    "repos": [],
    "users": ["abdielsouza"],
    "orgs": [],
}

async def scan_async(**kwargs):
    load_dotenv()

    if os.getenv("RUNNING_MODE") == "prod":
        client = GithubClient(token=str(os.getenv("GITHUB_TOKEN")))
        pipeline = RepositoryPipeline(
            client,
            PostgresStore(
                user=os.environ["POSTGRES_DB_USER"],
                host=os.environ["POSTGRES_DB_HOST"],
                port=os.environ["POSTGRES_DB_PORT"],
                dbname=os.environ["POSTGRES_DB_NAME"],
                password=os.environ["POSTGRES_DB_PASSWORD"],
            ),
            users=kwargs.get("users", TEST_DISCOVERY_INFO["users"]),
            orgs=kwargs.get("orgs", TEST_DISCOVERY_INFO["orgs"]),
            repos=kwargs.get("repos", TEST_DISCOVERY_INFO["repos"])
        )

        await pipeline.run()
    else:
        config = Config.load(Path("config/etl.toml").resolve())
        client = GithubClient(token=config.github.token)
        
        pipeline = RepositoryPipeline(
            client,
            DuckDBStore(Path(config.database.path).resolve()),
            users=config.github.users,
            orgs=config.github.orgs,
            repos=config.github.repos
        )
        
        await pipeline.run()

@app.command()
def scan():
    asyncio.run(scan_async())

if __name__ == '__main__':
    app()