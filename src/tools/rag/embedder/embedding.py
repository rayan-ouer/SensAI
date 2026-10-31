import sys
from time import sleep

import numpy as np
import requests

from ..chunker.interfaces import Chunk
from .errors import EmbeddingError
from .variables import CHUNKS_PER_REQUEST, MAX_RETRIES, MODEL, OLLAMA_URL, TIMEOUT


def _normalize_vector(matrix: np.ndarray) -> np.ndarray:
    length = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(length == 0):
        raise EmbeddingError("Null vector received from Ollama")
    return matrix / length


def _print_progress(completed_chunks: int, total_chunks: int) -> None:
    percentage = completed_chunks / total_chunks * 100 if total_chunks else 0
    bar_width = 50
    filled_width = int(bar_width * percentage / 100)
    bar = "#" * filled_width + "-" * (bar_width - filled_width)
    print(
        f"\rEmbedding of {completed_chunks}/{total_chunks} chunks",
        end="",
        flush=True,
        file=sys.stderr,
    )


class Embedder:
    """Embeds texts with the same Ollama model used to index documents."""

    def __init__(
        self,
        model: str = MODEL,
        url: str = OLLAMA_URL,
        timeout: int = TIMEOUT,
        chunks_per_request: int = CHUNKS_PER_REQUEST,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        self.model = model
        self.url = url
        self.timeout = timeout
        self.chunks_per_request = chunks_per_request
        self.max_retries = max_retries

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            raise EmbeddingError("Empty text list")
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.chunks_per_request):
            if len(texts) > 1:
                _print_progress(start, len(texts))
            batch = texts[start : start + self.chunks_per_request]
            vectors.extend(self._embed_batch(batch))
        if len(vectors) != len(texts):
            raise EmbeddingError(f"got {len(vectors)} vectors for {len(texts)} texts")
        matrix = _normalize_vector(np.array(vectors, dtype=np.float32))
        return matrix.tolist()

    def embed_chunks(self, chunks: list[Chunk]) -> np.ndarray:
        if not chunks:
            raise EmbeddingError("Empty chunk list")
        return np.array(self.embed([chunk.text for chunk in chunks]), dtype=np.float32)

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        for attempt in range(self.max_retries):
            try:
                return self._send_request(texts)
            except EmbeddingError as error:
                if attempt == self.max_retries - 1:
                    raise EmbeddingError(f"{error}") from error
                sleep(2 * attempt)
        raise EmbeddingError("No embeddings received from Ollama")

    def _send_request(self, texts: list[str]) -> list[list[float]]:
        try:
            response = requests.post(
                f"{self.url}/api/embed",
                json={"model": self.model, "input": texts},
                timeout=self.timeout,
            )
        except requests.ConnectionError as error:
            raise EmbeddingError(
                "No Ollama response, check if it is launched (`ollama serve`) ?"
            ) from error
        except requests.Timeout as error:
            raise EmbeddingError(
                f"Timeout after {self.timeout}s, try reducing chunks per request"
            ) from error

        if response.status_code != 200:
            try:
                detail = response.json().get("error", response.text)
            except ValueError:
                detail = response.text
            raise EmbeddingError(f"{response.status_code}, {detail}")
        embeddings = response.json()["embeddings"]
        if len(embeddings) != len(texts):
            raise EmbeddingError(
                f"got {len(embeddings)} vectors for {len(texts)} texts"
            )
        return embeddings
