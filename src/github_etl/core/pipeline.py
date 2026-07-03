from abc import ABC
from .extractor import Extractor
from .transformer import Transformer
from .loader import Loader
from .reporter import PipelineReporter
import time

class AdaptedPerfCounter:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
    
    @property
    def elapsed(self):
        return self.end - self.start

class Pipeline(ABC):
    extractor: Extractor
    transformer: Transformer
    loader: Loader

    async def run(self):
        print("extracting repos...\n")

        with AdaptedPerfCounter() as t0:
            repositories = [repo for repo in await self.extractor.extract()]
        
        print(f"extraction elapsed time: {t0.elapsed}")

        reporter = PipelineReporter()
        reporter.start(len(repositories))

        for repo in repositories:
            try:
                transformed = self.transformer.transform(repo)
                self.loader.load(transformed)
                reporter.loaded()
            except:
                reporter.failed()
            finally:
                reporter.advance(repo["full_name"])
        
        reporter.finish()