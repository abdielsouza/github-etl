import polars as pl
from result import Ok, Err, Result

from .base import Stage

class TransformStage(Stage[Result[dict, Exception], pl.DataFrame]):
    async def process(self, item, metrics):
        try:
            if item.is_err():
                return Err(item.unwrap_err())

            repo = item.unwrap()

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
            })
            metrics.transformed += 1

            return Ok(df)

        except Exception as e:
            metrics.failed += 1
            return Err(e)