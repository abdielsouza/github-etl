import pytest
import polars as pl
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime
from result import Ok
from dataclasses import asdict

from github_etl.models import RepositoryData
from github_etl.stages import TransformStage, LoadStage
from github_etl.warehouse import Warehouse
from github_etl.core.metrics import PipelineMetrics
from github_etl.stores import DuckDBStore

@pytest.fixture
def repositories():
    return [
        RepositoryData(
            id="1",
            name="repo1",
            owner="abdiel",
            stars=10,
            forks=2,
            watchers=5,
            language="Python",
            open_issues=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        RepositoryData(
            id="2",
            name="repo2",
            owner="abdiel",
            stars=20,
            forks=3,
            watchers=8,
            language="Rust",
            open_issues=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]

@pytest.fixture
def metrics():
    return PipelineMetrics()

@pytest.mark.asyncio
async def test_transform_stage(repositories, metrics):
    stage = TransformStage()
    results = []

    for repo in repositories:
        transform_result = await stage.process(Ok(repo), metrics=metrics)
        assert transform_result.is_ok(), "failed to get transformed data"

        results.append(transform_result.unwrap())

    df = pl.DataFrame([repo for repo in results])

    assert df.height == 2, "expected 2 repositories in the generated dataframe."
    assert "name" in df.columns, "missing relevant data in the generated dataframe."
    assert df["stars"].sum() == 30, "missing relevant data in the generated dataframe."

@pytest.mark.asyncio
async def test_load_stage(repositories, metrics):
    with TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.duckdb"
        load_stage = LoadStage(DuckDBStore(db))
    
        transform_stage = TransformStage()
        results = []

        for repo in repositories:
            transform_result = await transform_stage.process(Ok(repo), metrics=metrics)
            assert transform_result.is_ok(), "failed to get transformed data"

            results.append(transform_result.unwrap())

        df = pl.DataFrame([repo for repo in results])

        await load_stage.process(Ok(df), metrics)

        warehouse = Warehouse(DuckDBStore(db))
        result = await warehouse.query(
            "repositories",
            "SELECT COUNT(*) AS total FROM repositories"
        )

        assert result["total"][0] == 2, "failed to load some data."

@pytest.mark.asyncio
async def test_load_stage_with_overwrite(repositories, metrics):
    with TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.duckdb"
        load_stage = LoadStage(DuckDBStore(db))
    
        transform_stage = TransformStage()
        results = []

        for repo in repositories:
            transform_result = await transform_stage.process(Ok(repo), metrics=metrics)
            assert transform_result.is_ok(), "failed to get transformed data"

            results.append(transform_result.unwrap())

        df = pl.DataFrame([repo for repo in results])

        await load_stage.process(Ok(df), metrics)
        await load_stage.process(Ok(df), metrics)

        warehouse = Warehouse(DuckDBStore(db))
        result = await warehouse.query(
            "repositories",
            "SELECT COUNT(*) AS total FROM repositories"
        )

        assert result["total"][0] == 2, "failed to load some data."