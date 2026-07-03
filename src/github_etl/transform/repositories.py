from github_etl.core.transformer import Transformer
import polars as pl

class RepositoryTransformer(Transformer):
    def transform(self, data):
        repo = data
        
        return pl.DataFrame({
            "id": [repo["id"]],
            "name": [repo["name"]],
            "owner": [repo["owner"]["login"]],
            "stars": [repo["stargazers_count"]],
            "forks": [repo["forks_count"]],
            "watchers": [repo["watchers_count"]],
            "language": [repo["language"]],
            "open_issues": [repo["open_issues"]],
            "created_at": [repo["created_at"]],
            "updated_at": [repo["updated_at"]],
        })