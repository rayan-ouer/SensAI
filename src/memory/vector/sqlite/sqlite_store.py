import json
import sqlite3

import sqlite_vec
from sqlite_vec import serialize_float32

from memory.vector.sqlite.models import VectorRecord
from core.vector import IVectorStore, VectorDocument, VectorMatch
from agent.errors import AppError


MODEL_NAME = "bge-m3"
VECTOR_DIMENSION = 1024
TABLE_NAME = "vectors"


class VectorStoreError(AppError):
    """Exception class when a vector store operation fails."""
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class SQLiteStore(IVectorStore):
    def __init__(
        self,
        db_path: str,
        model_name: str = MODEL_NAME,
        vector_dimension: int = VECTOR_DIMENSION,
        table_name: str = TABLE_NAME,
    ):
        self._model_name = model_name
        self._vector_dimension = vector_dimension
        self._table_name = table_name
        self._db = sqlite3.connect(db_path)
        self._db.enable_load_extension(True)
        sqlite_vec.load(self._db)
        self._db.execute("PRAGMA journal_mode=WAL")
        self.create_table()

    def _create_table(self) -> None:
        self
    
    def _verify_embeddings(self, embeddings: list[list[float]]) -> None:
        if not embeddings:
            raise VectorStoreError("No embeddings provided")

        for embedding in embeddings:
            if len(embedding) != self._vector_dimension:
                raise VectorStoreError(f"Embedding dimension mismatch: {len(embedding)} != {self._vector_dimension}")

    def add(self, documents: list[VectorDocument]) -> None:
        if not documents:
            raise VectorStoreError("No documents provided")
        self._verify_embeddings([document.embedding for document in documents])
        ids: list[tuple[str]] = [(document.id, ) for document in documents]

        with self._db:
            self._db.executemany(f"DELETE FROM {self._table_name}_vec WHERE id = ?", ids)
            self._db.executemany(f"DELETE FROM {self._table_name} WHERE id = ?", ids)
            self._db.executemany(f"INSERT INTO {self._table_name}(id, content, source, meta) VALUES (?, ?, ?, ?)",
            [(d.id, d.content, d.source, json.dumps(d.meta)) for d in documents])
            self._db.executemany(f"INSERT INTO {self._table_name}_vec(id, embedding) VALUES (?, ?)",
            [(d.id, serialize_float32(d.embedding)) for d in documents])

    def search(self, query: str, top_k: int) -> list[VectorMatch]:
        statement = select(VectorRecord).order_by(VectorRecord.embedding.cosine_similarity(query)).limit(top_k)
        result = self._db_connection.execute(statement)

        return [VectorMatch(
            id=row.id,
            content=row.content,
            score=row.embedding.cosine_similarity(query),
            source=row.source,
            meta=row.meta,
        ) for row in result]
