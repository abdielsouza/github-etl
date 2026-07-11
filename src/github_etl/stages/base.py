from abc import ABC, abstractmethod
from result import Result

from github_etl.core.metrics import PipelineMetrics

class Stage[Input, Output, MetricsType = PipelineMetrics, ErrType = Exception](ABC):
    @abstractmethod
    async def process(self, item: Input, metrics: MetricsType) -> Result[Output, ErrType]:
        ...