from dataclasses import dataclass, field
from time import perf_counter
from typing import Optional

@dataclass
class PipelineMetrics:
    discovered:     int             = 0
    processed:      int             = 0
    loaded:         int             = 0
    failed:         int             = 0
    started_at:     float           = field(default_factory=perf_counter)
    finished_at:    Optional[float] = None

    @property
    def elapsed(self) -> float:
        if self.finished_at is None:
            return perf_counter() - self.started_at
        
        return self.finished_at - self.started_at
    
    @property
    def rate(self) -> float:
        if self.elapsed == 0:
            return 0
        
        return self.processed / self.elapsed