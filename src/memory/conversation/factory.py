from enum import Enum
from typing import Callable

from sqlalchemy.orm import Session

from core.conversation import IConversation
from memory.conversation.in_database import DatabaseConversation
from memory.conversation.in_memory import InMemoryConversation


class ConversationStorage(str, Enum):
    MEMORY: str = "memory"
    DATABASE: str = "database"

STORAGE_MAP: dict[ConversationStorage, Callable[[], IConversation]] = {
    ConversationStorage.MEMORY: InMemoryConversation.create_conversation,
    ConversationStorage.DATABASE: DatabaseConversation.create_conversation,
}


class ConversationFactory:
    """Builds a conversation store for the requested storage backend."""

    @staticmethod
    def create(
        storage: ConversationStorage,
        session: Session | None = None,
    ) -> IConversation:
        return STORAGE_MAP[storage](conversation_id, user_id, system_prompt)

    @staticmethod
    def _create_memory() -> IConversation:
        return InMemoryConversation()

    @staticmethod
    def _create_database(session: Session | None) -> IConversation:
        if session is None:
            raise ValueError("A database session is required for database storage")
        return DatabaseConversation(session)
