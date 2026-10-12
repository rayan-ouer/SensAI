from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from memory.vector.interface import (
    IVectorDB,
    VectorDocument,
    VectorMatch,
    validate_embedding,
)

from .models import VectorRecord


class PostgresVectorDB(IVectorDB):
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
            record.embedding = document.embedding
            record.source = document.source
            record.meta = document.meta

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
        source: Optional[str] = None,
    ) -> list[VectorMatch]:
        validate_embedding(embedding)
        distance = VectorRecord.embedding.cosine_distance(embedding)
        statement = select(VectorRecord, distance.label("distance"))
        if source is not None:
            statement = statement.where(VectorRecord.source == source)
        statement = statement.order_by(distance).limit(limit)

        matches: list[VectorMatch] = []
        for record, raw_distance in self._db.execute(statement):
            matches.append(
                VectorMatch(
                    document=self._to_document(record),
                    score=1 - float(raw_distance),
                )
            )
        return matches

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
            embedding=document.embedding,
            source=document.source,
            meta=document.meta,
        )

    def _to_document(self, record: VectorRecord) -> VectorDocument:
        return VectorDocument(
            id=record.id,
            content=record.content,
            embedding=list(record.embedding),
            source=record.source,
            meta=dict(record.meta),
        )
