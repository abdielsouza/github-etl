import polars as pl
from result import Ok, Err, Result
from dataclasses import asdict

from .base import Stage
from ..models import RepositoryData

class TransformStage(Stage[Result[dict | RepositoryData, Exception], pl.DataFrame]):
    async def process(self, item, metrics):
        try:
            if item.is_err():
                return Err(item.unwrap_err())

            repo = item.unwrap()
            
            if isinstance(repo, dict):
                df = pl.DataFrame({
                    "id":           [repo["id"]],
                    "name":         [repo["name"]],
                    "owner":        [repo["owner"]["login"]],
                    "stars":        [repo["stargazers_count"]],
                    "forks":        [repo["forks_count"]],
                    "watchers":     [repo["watchers_count"]],
                    "language":     [repo["language"]],
                    "open_issues":  [repo["open_issues"]],
                    "created_at":   [repo["created_at"]],
                    "updated_at":   [repo["updated_at"]],
                },
                schema={
                    "id":           pl.Int64,
                    "name":         pl.String,
                    "owner":        pl.String,
                    "stars":        pl.Int64,
                    "forks":        pl.Int64,
                    "watchers":     pl.Int64,
                    "language":     pl.String,
                    "open_issues":  pl.Int64,
                    "created_at":   pl.String,
                    "updated_at":   pl.String,
                })
            else:
                df = pl.DataFrame([asdict(repo)])
            
            metrics.transformed += 1

            return Ok(df)

        except Exception as e:
            metrics.add_error(
                stage="transform",
                message=str(e),
            )
            return Err(e)