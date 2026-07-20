from dataclasses import dataclass, field
from time import perf_counter
from typing import Optional

from .errors import PipelineError

@dataclass(slots=True)
class PipelineMetrics:
    discovered: int = 0
    extracted: int = 0
    transformed: int = 0
    loaded: int = 0
    failed: int = 0
    started_at: float = field(default_factory=perf_counter)
    finished_at: Optional[float] = None
    errors: list[PipelineError] = field(default_factory=list)

    @property
    def elapsed(self) -> float:
        if self.finished_at is None:
            return perf_counter() - self.started_at

        return self.finished_at - self.started_at
    
    @property
    def throughput(self) -> float:
        if self.elapsed == 0:
            return 0

        return self.loaded / self.elapsed

    def add_error(self, stage: str, message: str, item: Optional[str] = None):
        self.failed += 1
        self.errors.append(
            PipelineError(stage=stage, message=message, item=item)
        )