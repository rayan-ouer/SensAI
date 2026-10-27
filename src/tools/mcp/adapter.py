##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## adapter
##

from typing import Any

from core.tools import ITool

from .client import MCPClient


def _schema(spec: Any) -> dict[str, Any]:
    schema = getattr(spec, "input_schema", None)
    if schema is None:
        schema = getattr(spec, "inputSchema", None)
    if isinstance(schema, dict):
        return schema
    return {"type": "object", "properties": {}}


class MCPTool(ITool):
    def __init__(
        self, client: MCPClient, name: str, description: str, args: dict[str, Any]
    ):
        self._client = client
        self._name = name
        self._description = description
        self._args = args

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def args(self) -> dict[str, Any]:
        return self._args

    def run(self, arguments: dict[str, Any]) -> str:
        return self._client.call_tool(self._name, arguments)


class MCPAdapter:
    def __init__(self, client: MCPClient):
        self._client = client

    def list_tools(self) -> list[ITool]:
        return [
            MCPTool(
                self._client,
                spec.name,
                spec.description or "",
                _schema(spec),
            )
            for spec in self._client.list_tools()
        ]
