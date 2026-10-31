from enum import Enum
from pathlib import Path

from core.vector import IVectorStore


class VectorStoreKind(str, Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class VectorStoreFactory:
    def __init__(self) -> None:
        self._stores = {
            VectorStoreKind.SQLITE: self.create_sqlite,
        }

    def create(self, kind: VectorStoreKind, location: str) -> IVectorStore:
        builder = self._stores.get(kind)
        if builder is None:
            raise ValueError(f"Vector store '{kind.value}' is not available")
        return builder(location)

    @staticmethod
    def create_sqlite(location: str) -> IVectorStore:
        from memory.vector.sqlite.sqlite_store import SQLiteStore

        Path(location).parent.mkdir(parents=True, exist_ok=True)
        return SQLiteStore(location)
