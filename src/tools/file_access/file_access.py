##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## file_access
##

from pathlib import Path

from fastmcp import FastMCP

from core.tools import ITool
from tools.chat.config_data import ConfigData
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
        """Write complete UTF-8 content after explicit user approval.

        path: File path relative to the workspace root.
        content: Complete new content.

        The user is prompted for Y/N confirmation for every write, including
        creating a new file or overwriting an existing one. A declined write is
        cancelled. The path must have a matching workspace permission.
        """
        return workspace.write_in_file(path, content)

    return mcp


def create_workspace(config: ConfigData) -> WorkspaceSession:
    root = Path.cwd()
    permissions_path = Path(config.config_dir, config.file_access_config)
    try:
        workspace = WorkspaceSession(root, permissions_path)
    except OSError as error:
        raise ConfigError(
            f"cannot initialize file workspace: {error}", root
        ) from error
    print(f"Working directory: {workspace.root}")
    return workspace


def create_file_access_tools(workspace: WorkspaceSession) -> list[ITool]:
    return MCPAdapter(MCPClient(create_file_access_server(workspace))).list_tools()


def build_workspace_context(workspace: WorkspaceSession) -> str:
    return f"\n## Workspace context\n{workspace.initial_context()}\n"
