from enum import Enum

from fastapi import Depends
from sqlalchemy.orm import Session

from core.conversation import IConversationService
from memory.conversation.in_database import DatabaseConversation
from memory.conversation.in_memory import InMemoryConversation
from memory.database import get_db_session


class ConversationStorage(str, Enum):
    MEMORY: str = "memory"
    DATABASE: str = "database"


class ConversationServiceFactory:
    def __init__(self):
        self.CONVERSATION_SERVICE_MAP = {
            ConversationStorage.MEMORY: self.create_memory,
            ConversationStorage.DATABASE: self.create_database,
        }

    def create(self, storage: ConversationStorage) -> IConversationService:
        return self.CONVERSATION_SERVICE_MAP[storage]()

    @staticmethod
    def create_memory() -> IConversationService:
        return InMemoryConversation()

    @staticmethod
    def create_database() -> IConversationService:
        session: Session = Depends(get_db_session)
        return DatabaseConversation(session)
