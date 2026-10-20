from dataclasses import dataclass


@dataclass()
class ToolContext:
    """Dependencies and context for tools."""

    sandbox_session_id: str | None = None
