from dataclasses import dataclass
from typing import Optional

@dataclass
class PipelineError:
    stage: str
    message: str
    item: Optional[str] = None