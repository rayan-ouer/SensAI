from sqlalchemy import JSON, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from memory.base import Base


class VectorRecord(Base):
    __tablename__ = "vector_documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False, index=True)
    meta: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)