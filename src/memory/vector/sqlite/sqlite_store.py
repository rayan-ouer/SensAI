import json
import sqlite3
from typing import Any

import sqlite_vec
from sqlite_vec import serialize_float32

from core.vector import DEFAULT_TOP_K, IVectorStore, VectorDocument, VectorMatch
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
        self._db.enable_load_extension(False)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._create_table()

    def _create_table(self) -> None:
        self._db.executescript(f"""
            CREATE TABLE IF NOT EXISTS {self._table_name} (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                meta TEXT NOT NULL DEFAULT '{{}}'
            );
            CREATE INDEX IF NOT EXISTS idx_{self._table_name}_source ON {self._table_name}(source);
            CREATE VIRTUAL TABLE IF NOT EXISTS {self._table_name}_vec USING vec0(
                id TEXT PRIMARY KEY,
                embedding float[{self._vector_dimension}] distance_metric=cosine
            );
        """)
    
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

    def search(
        self,
        query_embedding: list[float],
        top_k: int = DEFAULT_TOP_K,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorMatch]:
        self._verify_embeddings([query_embedding])

        where, filter_params = self._create_filter_statement(filters)
        statement = f"""
            SELECT d.id, d.content, d.source, d.meta, v.distance
            FROM (
                SELECT id, distance
                FROM {self._table_name}_vec
                WHERE embedding MATCH ?
                  AND k = ?
            ) AS v
            JOIN {self._table_name} AS d ON d.id = v.id
            {where}
            ORDER BY v.distance
        """

        rows = self._db.execute(
            statement,
            [serialize_float32(query_embedding), top_k, *filter_params],
        ).fetchall()
        return [
            VectorMatch(
                id=row[0],
                content=row[1],
                score=1.0 - float(row[4]),
                source=row[2],
                meta=json.loads(row[3]) if row[3] else {},
            )
            for row in rows
        ]

    def _create_filter_statement(self, filters: dict[str, Any] | None) -> tuple[str, list[Any]]:
        if not filters:
            return "", []

        clauses: list[str] = []
        params: list[Any] = []
        for key, value in filters.items():
            if not str(key).isidentifier():
                raise VectorStoreError(f"Invalid filter key: {key}")
            if key == "source":
                clauses.append("d.source = ?")
                params.append(value)
            else:
                clauses.append("json_extract(d.meta, ?) = ?")
                params.extend((f"$.{key}", value))
        return "WHERE " + " AND ".join(clauses), params
