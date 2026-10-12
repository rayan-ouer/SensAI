"""Vector database package."""

from .factory import create_vector_db
from .interface import EMBEDDING_DIMENSION, IVectorDB, VectorDocument, VectorMatch

__all__ = [
    "EMBEDDING_DIMENSION",
    "IVectorDB",
    "VectorDocument",
    "VectorMatch",
    "create_vector_db",
]
