from .file_conversation import FileConversation
from .iconversation import (
    ConversationError,
    ConversationNotFoundError,
    IConversation,
    MessageError,
    MessageNotFoundError,
)

__all__ = [
    "ConversationError",
    "ConversationNotFoundError",
    "DatabaseConversation",
    "FileConversation",
    "IConversation",
    "MessageError",
    "MessageNotFoundError",
]


def __getattr__(name):
    if name == "DatabaseConversation":
        from .db_conversation import DatabaseConversation

        return DatabaseConversation
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
