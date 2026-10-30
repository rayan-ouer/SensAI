from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from memory.base import Base

EMBEDDING_DIMENSION = 1024


class VectorRecord(Base):
    __tablename__ = "vector_documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(
        Vector(EMBEDDING_DIMENSION),
        nullable=False,
    )
    source: Mapped[str] = mapped_column(String, nullable=False, index=True)
    meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
