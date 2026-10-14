from sqlalchemy import BLOB, JSON, Column, Integer

from memory.base import Base


class Vector(Base):
    __tablename__ = "vectors"
    id = Column(Integer, primary_key=True)
    embedding = Column(BLOB)
    metadata = Column(JSON)
