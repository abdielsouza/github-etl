import tomllib

from pathlib import Path
from pydantic import BaseModel

class GithubConfig(BaseModel):
    token: str
    users: list[str] = []
    repos: list[str] = []
    orgs: list[str] = []

class DatabaseConfig(BaseModel):
    path: str

class PipelineConfig(BaseModel):
    batch_size: int = 100

class Config(BaseModel):
    github: GithubConfig
    database: DatabaseConfig
    pipeline: PipelineConfig

    @classmethod
    def load(cls, path: str | Path) -> Config:
        with open(path, "rb") as file:
            data = tomllib.load(file)
        
        return cls.model_validate(data)
