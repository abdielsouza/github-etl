from github_etl.core.metrics import PipelineMetrics

from abc import ABC, abstractmethod

class Pipeline(ABC):
    def __init__(self):
        self._metrics = PipelineMetrics()
    
    @abstractmethod
    async def run(self) -> None: ...