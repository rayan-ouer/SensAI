from fastmcp import FastMCP

from core.vector import VectorMatch

def create_rag_server() -> FastMCP:
    mcp = FastMCP("sensai-rag")

    @mcp.tool
    def search_documents(query: str) -> list[VectorMatch]:
        return []

    return mcp