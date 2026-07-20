import polars as pl
import traceback
from result import Ok, Err, Result

from .base import Stage
from ..stores import RepositoryStore

class LoadStage(Stage[Result[pl.DataFrame, Exception], None]):
    def __init__(self, store: RepositoryStore):
        self._store = store
        self._buffer = []
        self._batch_size = 10

    async def process(self, item, metrics):
        try:
            if item.is_err():
                return Err(item.unwrap_err())
            
            df = item.unwrap()
            self._buffer.append(df)

            if len(self._buffer) >= self._batch_size or metrics.loaded + len(self._buffer) >= metrics.extracted:
                await self._flush(metrics)

            return Ok(None)
        
        except Exception as e:
            metrics.add_error(
                stage="load",
                message=traceback.format_exc(),
            )
            return Err(e)
    
    def close_connection(self):
        pass

    async def _flush(self, metrics):
        if not self._buffer:
            return
        
        batch = pl.concat(self._buffer)
        await self._store.write(batch)
        
        metrics.loaded += len(self._buffer)

        self._buffer.clear()