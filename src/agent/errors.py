##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## errors
##

from pathlib import Path

from tools.chat.errors import AppError


class AgentConfigError(AppError):
    """Exception class when a agents configuration is invalid."""
    def __init__(self, path: str):
        super().__init__(f"Invalid agents configuration: {path}")
