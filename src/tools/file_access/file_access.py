from pathlib import Path

from fastmcp import FastMCP

from core.tools import ToolHandler
from tools.chat.errors import ConfigError
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient

from .workspace import WorkspaceSession

def create_file_access_server(workspace: WorkspaceSession) -> FastMCP:
    mcp = FastMCP("sensai-file-access")

    @mcp.tool(name="list")
    def list_directory(path: str = ".") -> str:
        """List entries in a directory inside the confirmed workspace.

        path: Directory path relative to the workspace root.
        """
        return workspace.list_directory(path)

    @mcp.tool
    def read_file(path: str) -> str:
        """Read a text file allowed by the workspace permissions.

        path: File path relative to the workspace root.
        """
        return workspace.read_file(path)

    @mcp.tool
    def create_file(path: str, content: str) -> str:
        """Create a new text file; existing files are never overwritten.

        path: File path relative to the workspace root.
        content: Text to write to the new file.
        """
        return workspace.create_file(path, content)

    @mcp.tool
    def write_in_file(path: str, content: str) -> str:
        """Replace a file's entire UTF-8 text content, creating it if absent.

        path: File path relative to the workspace root.
        content: Complete new content. Existing content is overwritten.
        """
        return workspace.write_in_file(path, content)
    return mcp


def create_workspace(config: dict) -> WorkspaceSession:
    root = Path.cwd()
    permissions_path = Path(
        config["config_dir"], config.get("file_access_config", "file_access.yaml")
    )
    try:
        workspace = WorkspaceSession(root, permissions_path)
    except OSError as error:
        raise ConfigError(
            f"cannot initialize file workspace: {error}", root
        ) from error
    print(f"Working directory: {workspace.root}")
    return workspace


def register_file_access_tools(
    manager: ToolHandler, workspace: WorkspaceSession
) -> None:
    adapter = MCPAdapter(MCPClient(create_file_access_server(workspace)))
    manager.register_many(adapter.list_tools())
