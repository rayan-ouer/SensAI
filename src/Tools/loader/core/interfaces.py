from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

@dataclass
class Document:
    """Document is returned by the loader, no matter which file type it comes from."""
    text: str
    source: str
    position: int = 0
    kind: str = "long_text"
    meta: dict = field(default_factory=dict)

class BaseLoader(ABC):
    """Interface for loader classes."""
    extensions: tuple[str, ...] = ()
    _registry: dict[str, type["BaseLoader"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for ext in cls.extensions:
            cls._registry[ext.lower()] = cls

    def __init__(self, path: Path):
        self.path = Path(path)

    @abstractmethod
    def load(self) -> Iterator[Document]: ...

    @classmethod
    def available_formats(cls) -> list[str]:
        return sorted(BaseLoader._registry)

    @classmethod
    def for_path(cls, path: Path) -> "BaseLoader | None":
        loader_cls = BaseLoader._registry.get(Path(path).suffix.lower())
        return loader_cls(path) if loader_cls else None
