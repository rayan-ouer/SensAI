import sys
import json
from pathlib import Path

from core.tools import ITool
from tools.chat.errors import ConfigError
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient

class MCPLoader:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load_mcp_config(self) -> dict:
        servers = {}
        config = {}

        if not self.path.is_file():
            return {}
        try:
            with open(self.path, "r") as file:
                config = json.load(file)
        except json.JSONDecodeError:
            raise ConfigError("Invalid JSON format in MCP config file", self.path)
        return servers


def create_external_tools(path: str | Path) -> list[ITool]:
    try:
        config = MCPLoader(path).load_mcp_config()
    except ConfigError as e:
        print(e, file=sys.stderr)
        return []
    if not config.get("mcpServers"):
        return []
    return MCPAdapter(MCPClient(config)).list_tools()