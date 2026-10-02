from abc import ABC
from typing import Optional, Sequence

from sqlalchemy import literal, select
from sqlalchemy.orm import Session

from app.db.models import Conversation, Message, ToolCall as DBToolCall
from .messages import AIMessage, HumanMessage, SystemMessage, IMessage


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
    def __init__(self, session: Session) -> None:
        self._db: Session = session

    """Getters"""

    def get_conversation_by_id_or_none(self, conversation_id: str) -> Optional[Conversation]:
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = self._db.execute(statement)

        return result.scalar_one_or_none()

    def get_message_by_id_or_none(self, message_id: str) -> Optional[Message]:
        statement = select(Message).where(Message.id == message_id)
        result = self._db.execute(statement)

        return result.scalar_one_or_none()

    def get_conversation_by_id(self, conversation_id: str) -> Conversation:
        conversation: Optional[Conversation] = self.get_conversation_by_id_or_none(conversation_id)

        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        return conversation
    
    def get_message_by_id(self, message_id: str) -> Message:
        db_message: Optional[Message] = self.get_message_by_id_or_none(message_id)

        if not db_message:
            raise MessageNotFoundError(message_id)
        return db_message

    def get_active_message(self, conversation_id: str) -> Optional[Message]:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        return conversation.active_message
    
    def get_full_history(self, conversation_id: str) -> Sequence[Message]:
        _ = self.get_conversation_by_id(conversation_id)
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        result = self._db.execute(statement)

        return result.scalars().all()

    def get_used_history(self, conversation_id: str) -> Sequence[Message]:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        history = (
            select(
                Message.id,
                Message.parent_id,
                literal(0).label("depth"),
            )
            .where(Message.id == conversation.active_message_id)
            .cte("history", recursive=True)
        )
        parent = (
            select(
                Message.id,
                Message.parent_id,
                (history.c.depth + 1).label("depth"),
            )
            .join(history, Message.id == history.c.parent_id)
        )
        history = history.union_all(parent)
        statement = (
            select(Message)
            .join(history, Message.id == history.c.id)
            .order_by(history.c.depth.desc())
        )
        result = self._db.execute(statement)
        return result.scalars().all()

    """Small generics function to handle data."""
    def _create_db_message(self, conversation_id: str, message: IMessage) -> Message:
        return Message(
            conversation_id=conversation_id,
            role=message.role,
            content=message.content
        )

    """Business Logic"""

    def add_message(self, conversation_id: str, message: IMessage) -> Message:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        db_message: Message = self._create_db_message(conversation_id, message)

        db_message.parent_id = conversation.active_message_id
        conversation.active_message = db_message
        self._db.add(db_message)
        return db_message

    def edit_message(self, conversation_id: str, message_id: str, message: IMessage) -> Message:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        old_message: Message = self.get_message_by_id(message_id)

        db_message: Message = self._create_db_message(conversation_id, message)
        db_message.parent_id = old_message.parent_id
        conversation.active_message = db_message
        self._db.add(db_message)
        return db_message

    def add_ai_message(self, conversation_id: str, message: AIMessage) -> Message:
        db_message: Message = self.add_message(conversation_id, message)

        db_message.tool_calls.extend(
            self._create_db_tool_call(tool_call)
            for tool_call in message.tool_calls)
        return db_message

    def add_human_message(self, conversation_id: str, message: HumanMessage) -> Message:
        return self.add_message(conversation_id, message)

    def add_system_message(self, conversation_id: str, message: IMessage) -> Message:
        return self.add_message(conversation_id, message)
    
    def clear(self, conversation_id: str) -> None:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        conversation.active_message = None
        self._db.delete(conversation)
        
