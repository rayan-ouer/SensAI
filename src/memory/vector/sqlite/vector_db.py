from typing import Optional

import numpy as np
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from memory.vector.interface import (
    EMBEDDING_DIMENSION,
    IVectorDB,
    VectorDocument,
    VectorMatch,
    validate_embedding,
)

from .models import VectorRecord


def _pack(embedding: list[float]) -> bytes:
    return np.asarray(embedding, dtype=np.float32).tobytes()


def _unpack(blob: bytes) -> np.ndarray:
    vector = np.frombuffer(blob, dtype=np.float32)
    if vector.shape != (EMBEDDING_DIMENSION,):
        raise ValueError("stored embedding has an unexpected dimension")
    return vector


class SqliteVectorDB(IVectorDB):
    def __init__(self, session: Session) -> None:
        self._db = session

    def upsert(self, documents: list[VectorDocument]) -> None:
        for document in documents:
            validate_embedding(document.embedding)
            record = self._db.get(VectorRecord, document.id)
            if record is None:
                self._db.add(self._to_record(document))
                continue
            record.content = document.content
            record.embedding = _pack(document.embedding)
            record.source = document.source
            record.meta = document.meta

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
        source: Optional[str] = None,
    ) -> list[VectorMatch]:
        validate_embedding(embedding)
        statement = select(VectorRecord)
        if source is not None:
            statement = statement.where(VectorRecord.source == source)
        records = list(self._db.scalars(statement))
        if not records:
            return []

        query = np.asarray(embedding, dtype=np.float32)
        query_norm = float(np.linalg.norm(query))
        if query_norm == 0:
            return []

        matrix = np.vstack([_unpack(record.embedding) for record in records])
        norms = np.linalg.norm(matrix, axis=1)
        norms[norms == 0] = np.inf
        scores = (matrix @ query) / (norms * query_norm)
        best_indexes = np.argsort(scores)[::-1][:limit]
        return [
            VectorMatch(
                document=self._to_document(records[int(index)]),
                score=float(scores[int(index)]),
            )
            for index in best_indexes
        ]

    def delete(self, document_id: str) -> None:
        record = self._db.get(VectorRecord, document_id)
        if record is not None:
            self._db.delete(record)

    def delete_by_source(self, source: str) -> None:
        self._db.execute(delete(VectorRecord).where(VectorRecord.source == source))

    def _to_record(self, document: VectorDocument) -> VectorRecord:
        return VectorRecord(
            id=document.id,
            content=document.content,
            embedding=_pack(document.embedding),
            source=document.source,
            meta=document.meta,
        )

    def _to_document(self, record: VectorRecord) -> VectorDocument:
        return VectorDocument(
            id=record.id,
            content=record.content,
            embedding=_unpack(record.embedding).tolist(),
            source=record.source,
            meta=dict(record.meta or {}),
        )
