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


def _send_request(texts: list[str]):
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": MODEL, "input": texts},
            timeout=TIMEOUT,
        )
    except requests.ConnectionError:
        raise EmbeddingError(
            "No Ollama response, check if it is launched (`ollama serve`) ?"
        )
    except requests.Timeout:
        raise EmbeddingError(
            f"Timeout after {TIMEOUT}s, try reducing chunks per request"
        )

    if response.status_code != 200:
        try:
            detail = response.json().get("error", response.text)
        except ValueError:
            detail = response.text
        raise EmbeddingError(f"{response.status_code}, {detail}")
    embeddings = response.json()["embeddings"]
    if len(embeddings) != len(texts):
        raise EmbeddingError(f"got {len(embeddings)} vectors for {len(texts)} texts")
    return embeddings


def embed_chunks(chunks: list[Chunk]) -> np.ndarray:
    texts = [c.text for c in chunks]
    if not texts or texts == []:
        raise EmbeddingError("Empty chunk list")
    vectors = []
    for i in range(0, len(texts), CHUNKS_PER_REQUEST):
        _print_progress(i, len(texts))
        batch = texts[i : i + CHUNKS_PER_REQUEST]
        response = []
        for y in range(MAX_RETRIES):
            try:
                response = _send_request(batch)
                break
            except EmbeddingError as e:
                if y == MAX_RETRIES - 1:
                    raise EmbeddingError(f"{e}")
                sleep(2 * y)
        vectors += response
    if len(vectors) != len(chunks):
        raise EmbeddingError(f"got {len(vectors)} vectors for {len(chunks)} chunks")
    matrix = np.array(vectors, dtype=np.float32)
    return _normalize_vector(matrix)
