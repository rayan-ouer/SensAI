import asyncio
from typing import Any

from fastmcp import Client, FastMCP


def _result_text(result: Any) -> str:
    data = getattr(result, "data", None)
    if isinstance(data, str):
        return data
    content = getattr(result, "content", None) or []
    parts = [block.text for block in content if getattr(block, "text", None)]
    if parts:
        return "\n".join(parts)
    if data is None:
        return ""
    return str(data)


class MCPClient:
    def __init__(self, server: FastMCP):
        self._server = server

    def list_tools(self) -> list[Any]:
        return asyncio.run(self._list_tools())

    def call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        return asyncio.run(self._call_tool(name, arguments or {}))

    async def _list_tools(self) -> list[Any]:
        async with Client(self._server) as client:
            return await client.list_tools()

    async def _call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        async with Client(self._server) as client:
            result = await client.call_tool(name, arguments)
            return _result_text(result)
