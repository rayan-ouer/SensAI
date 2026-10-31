from typing import Any

from core.vector import IVectorStore, VectorMatch
from sentence_transformers import CrossEncoder
from tools.rag.embedder.variables import DEFAULT_TOP_K

RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"


class Retriever:
    def __init__(self, store: IVectorStore, reranker: CrossEncoder):
        self._store = store
        self._reranker = reranker

    def retrieve(
        self,
        query: str,
        query_embedding: list[float],
        top_k: int = DEFAULT_TOP_K,
        candidates: int = 30,
        min_score: float | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[VectorMatch]:
        found: list[VectorMatch] = self._store.search(query_embedding, candidates, filters)

        if not found:
            return []
        scores = self._reranker.predict([(query, match.content) for match in found])
        ranked = sorted(zip(found, scores), key=lambda item: item[1], reverse=True)
        if min_score is not None:
            ranked = [item for item in ranked if item[1] >= min_score]
        return [
            VectorMatch(match.id, match.content, float(score), match.source, match.meta)
            for match, score in ranked[:top_k]
        ]


def create_retriever(store: IVectorStore) -> Retriever:
    return Retriever(store, CrossEncoder(RERANKER_MODEL))
