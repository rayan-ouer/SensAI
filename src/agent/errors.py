from pathlib import Path

from tools.chat.errors import AppError


class AgentConfigError(AppError):
    """Exception class when an agents configuration is invalid."""

    def __init__(self, message: str, path: str | Path | None = None):
        self.message = message
        self.path = path

    def __str__(self) -> str:
        if self.path is not None:
            return f"{self.message}: {self.path}"
        return self.message
