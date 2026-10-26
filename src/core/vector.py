from abc import ABC, abstractmethod


class VectorDocument:
    def __init__(
        self,
        id: str,
        content: str,
        embedding: list[float],
        source: str,
        meta: dict = None,
    ):
        self.id = id
        self.content = content
        self.embedding = embedding
        self.source = source
        self.meta = meta if meta else {}


class VectorMatch:
    def __init__(
        self, id: str, content: str, score: float, source: str, meta: dict = None
    ):
        self.id = id
        self.content = content
        self.score = score
        self.source = source
        self.meta = meta if meta else {}


class IVectorStore(ABC):
    @abstractmethod
    def add(self, documents: list) -> None:
        pass

    @abstractmethod
    def search(self, query: str, top_k: int) -> list[str]:
        pass
