import sqlite3

import numpy as np

from core.vector import IVectorStore

MODEL_NAME = "bge-m3"
VECTOR_DIMENSION = 1024
TABLE_NAME = "vectors"


class SQLiteStore(IVectorStore):
    def __init__(
        self,
        db_path: str,
        model_name: str = MODEL_NAME,
        vector_dimension: int = VECTOR_DIMENSION,
        table_name: str = TABLE_NAME,
        enable_extensions: bool = True,
    ):
        self._db_path = db_path
        self._model_name = model_name
        self._vector_dimension = vector_dimension
        self._table_name = table_name
        self._db_connection = sqlite3.connect(db_path)
        self._db_connection.enable_load_extension(enable_extensions)

    def add(self, embeddings: list[np.ndarray]) -> None:
        pass

    def search(self, query: str, top_k: int) -> list[str]:
        pass
