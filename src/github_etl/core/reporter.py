from time import perf_counter
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from .metrics import PipelineMetrics

class PipelineReporter:
    def __init__(self):
        self._console = Console()
        self._metrics = PipelineMetrics()
    
    def start(self, total: int):
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            console=self._console,
        )
        self._progress.start()

        self._task = self._progress.add_task("Processing repositories", total=total)
    
    def advance(self, repository: str):
        self._metrics.processed += 1

        self._progress.update(
            self._task,
            advance=1,
            description=f"Processing {repository}",
        )
    
    def loaded(self):
        self._metrics.loaded += 1
    
    def failed(self):
        self._metrics.failed += 1
    
    def finish(self):
        self._metrics.finished_at = perf_counter()
        self._progress.stop()

        self._console.print()
        self._console.print("[bold green]Pipeline completed![/bold green]")
        self._console.print(f"Repositories processed: {self._metrics.processed}")
        self._console.print(f"Loaded: {self._metrics.loaded}")
        self._console.print(f"Failed: {self._metrics.failed}")
        self._console.print(f"Rate: {self._metrics.rate:.2f} repos per second")