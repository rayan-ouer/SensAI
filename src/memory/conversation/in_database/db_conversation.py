import uuid

from sqlalchemy import literal, select
from sqlalchemy.orm import Session

from core.conversation import (
    ConversationNotFoundError,
    IConversationService,
    MessageNotFoundError,
)
from core.messages import AIMessage, HumanMessage, IMessage, SystemMessage
from core.tools import ToolCall
from core.types import ToolStatus

from .models import Conversation, Message
from .models import ToolCall as DbToolCall


class DatabaseConversation(IConversationService):
    def __init__(self, session: Session) -> None:
        self._db: Session = session

    def create_conversation(
        self,
        user_id: str,
        system_prompt: str | None = None,
    ) -> str:
        if not user_id:
            raise ValueError("user_id is required to create a database conversation")

        conversation = Conversation(
            id=uuid.uuid4(),
            user_id=user_id,
        )
        self._db.add(conversation)
        self._db.flush()

        created_id: str = str(conversation.id)
        if system_prompt:
            self.add_system_message(created_id, SystemMessage(content=system_prompt))
        return created_id

    """Getters"""

    def get_conversation_by_id_or_none(
        self, conversation_id: str
    ) -> Conversation | None:
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = self._db.execute(statement)

        return result.scalar_one_or_none()

    def get_message_by_id_or_none(
        self, conversation_id: str, message_id: str
    ) -> Message | None:
        statement = select(Message).where(
            Message.id == message_id,
            Message.conversation_id == conversation_id,
        )
        result = self._db.execute(statement)
        return result.scalar_one_or_none()

    def get_conversation_by_id(self, conversation_id: str) -> Conversation:
        conversation: Conversation | None = self.get_conversation_by_id_or_none(
            conversation_id
        )
        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        return conversation

    def get_message_by_id(self, conversation_id: str, message_id: str) -> Message:
        db_message: Message | None = self.get_message_by_id_or_none(
            conversation_id, message_id
        )

        if not db_message:
            raise MessageNotFoundError(message_id)
        return db_message

    def get_active_message(self, conversation_id: str) -> Message | None:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        return conversation.active_message

    def get_full_history(self, conversation_id: str) -> list[IMessage]:
        _ = self.get_conversation_by_id(conversation_id)
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        result = self._db.execute(statement)

        return result.scalars().all()

    def get_used_history(self, conversation_id: str) -> list[IMessage]:
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
        parent = select(
            Message.id,
            Message.parent_id,
            (history.c.depth + 1).label("depth"),
        ).join(history, Message.id == history.c.parent_id)
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
            conversation_id=conversation_id, role=message.role, content=message.content
        )

    def _create_db_tool_call(self, tool_call: ToolCall) -> DbToolCall:
        return DbToolCall(
            tool_call_id=tool_call.id,
            tool_name=tool_call.name,
            arguments=tool_call.arguments
            if isinstance(tool_call.arguments, dict)
            else {},
            status=ToolStatus.PENDING,
        )

    """Business Logic"""

    def add_message(self, conversation_id: str, message: IMessage) -> Message:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        db_message: Message = self._create_db_message(conversation_id, message)

        db_message.parent_id = conversation.active_message_id
        conversation.active_message = db_message
        self._db.add(db_message)
        return db_message

    def edit_message(
        self, conversation_id: str, message_id: str, message: IMessage
    ) -> Message:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        old_message: Message = self.get_message_by_id(conversation_id, message_id)

        db_message: Message = self._create_db_message(conversation_id, message)
        db_message.parent_id = old_message.parent_id
        conversation.active_message = db_message
        self._db.add(db_message)
        return db_message

    def add_ai_message(self, conversation_id: str, message: AIMessage) -> Message:
        db_message: Message = self.add_message(conversation_id, message)

        db_message.tool_calls.extend(
            self._create_db_tool_call(tool_call) for tool_call in message.tool_calls
        )
        return db_message

    def add_human_message(self, conversation_id: str, message: HumanMessage) -> Message:
        return self.add_message(conversation_id, message)

    def add_system_message(
        self, conversation_id: str, message: SystemMessage
    ) -> Message:
        return self.add_message(conversation_id, message)

    def clear(self, conversation_id: str) -> None:
        conversation: Conversation = self.get_conversation_by_id(conversation_id)
        conversation.active_message = None
        self._db.delete(conversation)
