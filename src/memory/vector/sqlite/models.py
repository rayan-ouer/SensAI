from sqlalchemy import JSON, LargeBinary, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class SqliteBase(DeclarativeBase):
    pass


class VectorRecord(SqliteBase):
    __tablename__ = "vector_documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False, index=True)
    meta: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
