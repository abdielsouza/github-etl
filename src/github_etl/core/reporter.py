from abc import ABC, abstractmethod
from .metrics import PipelineMetrics
from enum import StrEnum

class PipelineStage(StrEnum):
    DISCOVERY = "discovery"
    EXTRACTION = "extraction"
    TRANSFORMATION = "transformation"
    LOADING = "loading"

class PipelineReporter(ABC):
    @abstractmethod
    def start(self, *, metrics: PipelineMetrics) -> None:
       ...

    @abstractmethod
    def stage_started(self, *, stage: PipelineStage, total: int = 0) -> None:
        ...
    
    @abstractmethod
    def advance(self, *, stage: PipelineStage, amount: int = 1) -> None:
        ...
    
    @abstractmethod
    def stage_finished(self, *, stage: PipelineStage) -> None:
        ...
    
    @abstractmethod
    def refresh(self, *, metrics: PipelineMetrics) -> None:
        ...
    
    @abstractmethod
    def finish(self, *, metrics: PipelineMetrics) -> None:
        ...