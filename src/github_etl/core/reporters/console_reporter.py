from github_etl.core.metrics import PipelineMetrics
from github_etl.core.reporter import *

from time import perf_counter

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    SpinnerColumn,
    TextColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TaskID,
)

from github_etl.core.reporter import PipelineStage
from typing import cast

class ConsoleReporter(PipelineReporter):
    def __init__(self):
        self._console = Console()
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue] {task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._console,
        )
        self._tasks: dict[PipelineStage, int] = {}
        self._live = Live(
            self._progress,
            console=self._console,
            refresh_per_second=10,
        )
    
    def start(self, *, metrics):
        metrics.started_at = perf_counter()
        self._live.start()
    
    def stage_started(self, *, stage: PipelineStage, total: int = 0) -> None:
        task = self._progress.add_task(
            stage.value.capitalize(),
            total=total if total else None,
        )
        self._tasks[stage] = task
    
    def advance(self, *, stage: PipelineStage, amount: int = 1) -> None:
        self._progress.update(cast(TaskID, self._tasks[stage]), advance=amount)
    
    def stage_finished(self, *, stage: PipelineStage) -> None:
        self._progress.update(
            cast(TaskID, self._tasks[stage]),
            completed=self._progress.tasks[
                cast(TaskID, self._tasks[stage])
            ].total or 1,
        )
    
    def refresh(self, *, metrics) -> None:
        self._console.log(f"Processed: {metrics.loaded}")
    
    def finish(self, *, metrics) -> None:
        metrics.finished_at = perf_counter()
        self._live.stop()
        self._console.print()
        self._console.print(
            Panel.fit(
            f"""
            [bold green]Pipeline completed![/bold green]
            Repositories: {metrics.discovered}
            Extracted: {metrics.extracted}
            Transformed: {metrics.transformed}
            Loaded: {metrics.loaded}
            Failed: {metrics.failed}
            Elapsed: {metrics.elapsed:.2f}s
            Rate: {metrics.throughput:.2f} repos/s
            """,
            title="Summary"
            )
        )
    
    def print(self, content: str):
        self._console.print(content)