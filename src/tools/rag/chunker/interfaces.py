from dataclasses import dataclass, field


@dataclass
class Chunk:
    text: str
    source: str
    position: int = 0
    chunk_index: int = 0
    meta: dict = field(default_factory=dict)
