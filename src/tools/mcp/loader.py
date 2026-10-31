import json
from pathlib import Path

from core.tools import ITool
from tools.loader.core.errors import LoaderError
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient

class MCPLoader:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.is_file():
            raise LoaderError("File not found.", self.path)
    
    def load_mcp_config(self) -> dict:
        servers = {}

        with open(self.path, "r") as file:
            servers = json.load(file)
        return servers


def create_external_tools(path: str | Path) -> list[ITool]:
    config = MCPLoader(path).load_mcp_config()
    if not config.get("mcpServers"):
        return []
    return MCPAdapter(MCPClient(config)).list_tools()