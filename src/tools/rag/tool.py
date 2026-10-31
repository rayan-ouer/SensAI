from typing import Any

from fastmcp import FastMCP

from core.tools import ITool
from core.vector import IVectorStore, VectorMatch
from memory.vector.factory import VectorStoreFactory, VectorStoreKind
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient
from tools.rag.embedder.embedding import Embedder
from tools.rag.embedder.variables import DEFAULT_TOP_K
from tools.rag.retriever.retriever import Retriever, create_retriever


def build_rag_resources(
    location: str,
    kind: VectorStoreKind = VectorStoreKind.SQLITE,
) -> tuple[IVectorStore, Embedder, Retriever]:
    store = VectorStoreFactory().create(kind, location)
    return store, Embedder(), create_retriever(store)


def _format_matches(matches: list[VectorMatch]) -> str:
    if not matches:
        return "No matching passages."
    blocks = []
    for index, match in enumerate(matches, start=1):
        blocks.append(
            f"{index}. {match.source} (score: {match.score:.3f})\n{match.content}"
        )
    return "\n\n".join(blocks)


def create_rag_server(
    retriever: Retriever,
    embedder: Embedder,
    default_top_k: int = DEFAULT_TOP_K,
) -> FastMCP:
    mcp = FastMCP("sensai-rag")

    @mcp.tool
    def search_documents(
        query: str,
        top_k: int = default_top_k,
        filters: dict[str, Any] | None = None,
    ) -> str:
        """Search stored documents and return the closest passages.

        query: Question or words to look up in the indexed documents.
        top_k: Number of passages to return.
        filters: Optional metadata filters applied by the vector store.
        """
        text: str = query.strip()
        if not text:
            raise ValueError("query is required")
        embedding: list[float] = embedder.embed([text])[0]
        matches = retriever.retrieve(text, embedding, top_k=top_k, filters=filters)
        return _format_matches(matches)

    return mcp


def create_rag_tools(retriever: Retriever, embedder: Embedder) -> list[ITool]:
    server = create_rag_server(retriever, embedder)
    return MCPAdapter(MCPClient(server)).list_tools()
