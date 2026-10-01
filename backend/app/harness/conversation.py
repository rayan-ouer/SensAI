from abc import ABC
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Conversation, Message, ToolCall as DBToolCall
from .messages import AIMessage, HumanMessage, IMessage


class ConversationError(Exception):
    """Base exception for conversation-related errors."""


class ConversationNotFoundError(Exception):
    """Exception class when a conversation is not found."""

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        super().__init__(f"Conversation {conversation_id} not found.")


class MessageError(Exception):
    """Base exception for message-related errors."""


class MessageNotFoundError(Exception):
    """Exception class when a conversation is not found."""

    def __init__(self, message_id: str):
        self.message_id = message_id
        super().__init__(f"Message {message_id} not found.")



class IConversation(ABC):
    def add_message(message: IMessage):
        pass

    def add_ai_message(message: AIMessage):
        pass

    def add_human_message(message: HumanMessage):
        pass

    def get_used_history():
        pass

    def get_full_history():
        pass

    def get_conversation_by_id(id: str):
        pass

    def edit_message(message_id: str, _: IMessage):
        pass

    def clear():
        pass


class DatabaseConversation(IConversation):
    def __init__(self, session: Session):
        self._db: Session = session

    """Getters"""

    def get_conversation_by_id_or_none(self, conversation_id: str):
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = self._db.execute(statement)

        return result.scalar_one_or_none()

    def get_message_by_id_or_none(self, message_id: str):
        statement = select(Message).where(Message.id == message_id)
        result = self._db.execute(statement)

        return result.scalar_one_or_none()

    def get_conversation_by_id(self, conversation_id: str):
        conversation = self.get_conversation_by_id_or_none(conversation_id)

        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        return conversation
    
    def get_message_by_id(self, message_id: str):
        db_message = self.get_message_by_id_or_none(message_id)

        if not db_message:
            raise MessageNotFoundError(message_id)
        return db_message


    def get_used_history(self, conversation_id: str):
        conversation = self.get_conversation_by_id(conversation_id)

        if not conversation:
            raise ConversationNotFoundError(conversation_id)

    def get_full_history(self):
        pass

    """Small generics function to handle data."""
    def _create_message(self, conversation_id: str, message: IMessage):
        return Message(
            conversation_id=conversation_id,
            role=message.role,
            content=message.content
        )

    """Business Logic"""

    def add_message(self, conversation_id: str, message: IMessage) -> Message:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        db_message: Message = self._create_message(conversation_id, message)

        db_message.parent_id = conversation.active_message_id
        conversation.active_message = db_message
        self._db.add(db_message)
        return db_message

    def edit_message(self, conversation_id: str, message_id: str, message: IMessage):
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        old_message: Message = self.get_message_by_id(message_id)

        if not message:
            raise MessageNotFoundError(message_id)
        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        db_message: Message = self._create_message(conversation_id, new_message)
        message.content = new_message.content
        message.parent = 
        conversation.active_message = message


    def clear(self):
        pass
