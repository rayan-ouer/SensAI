from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

# bge-m3, the model used by the RAG embedder.
EMBEDDING_DIMENSION = 1024


@dataclass
class VectorDocument:
    id: str
    content: str
    embedding: list[float]
    source: str
    meta: dict = field(default_factory=dict)


@dataclass(frozen=True)
class VectorMatch:
    document: VectorDocument
    score: float


def validate_embedding(embedding: list[float]) -> None:
    if len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"expected an embedding of dimension {EMBEDDING_DIMENSION}, got {len(embedding)}"
        )


class IVectorDB(ABC):
    """Storage contract shared by the SQLite and PostgreSQL vector databases."""

    @abstractmethod
    def upsert(self, documents: list[VectorDocument]) -> None:
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        limit: int = 5,
        source: Optional[str] = None,
    ) -> list[VectorMatch]:
        pass

    @abstractmethod
    def delete(self, document_id: str) -> None:
        pass

    @abstractmethod
    def delete_by_source(self, source: str) -> None:
        pass
