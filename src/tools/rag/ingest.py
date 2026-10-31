from dataclasses import dataclass
from pathlib import Path

import tools.loader.type_loaders.csv_loader  # noqa: F401
import tools.loader.type_loaders.markdown_loader  # noqa: F401
import tools.loader.type_loaders.pdf_loader  # noqa: F401
import tools.loader.type_loaders.text_loader  # noqa: F401
from core.vector import IVectorStore, VectorDocument
from memory.vector.sqlite.sqlite_store import VectorStoreError
from tools.loader.core.errors import FileReaderError, LoaderError, UnsupportedFormat
from tools.loader.loader import FileReader
from tools.rag.chunker.chunker import Chunker
from tools.rag.embedder.embedding import Embedder
from tools.rag.embedder.errors import EmbeddingError

DOCUMENT_ERRORS = (LoaderError, UnsupportedFormat, FileReaderError, EmbeddingError, VectorStoreError)


@dataclass
class AddedDocument:
    source: str
    chunks: int


def add_document(path: str | Path, store: IVectorStore, embedder: Embedder) -> AddedDocument:
    file_path = Path(path)
    documents = list(FileReader(file_path).get_parser().load())
    chunks = Chunker(documents).chunk()
    if not chunks:
        raise LoaderError("Document is empty.", file_path)
    vectors = embedder.embed_chunks(chunks)
    source = str(file_path.resolve())
    stored = [
        VectorDocument(
            id=f"{source}#{index}",
            content=chunk.text,
            embedding=vectors[index].tolist(),
            source=source,
            meta={**chunk.meta, "position": chunk.position, "chunk_index": chunk.chunk_index},
        )
        for index, chunk in enumerate(chunks)
    ]
    store.delete_source(source)
    store.add(stored)
    return AddedDocument(source=source, chunks=len(stored))
