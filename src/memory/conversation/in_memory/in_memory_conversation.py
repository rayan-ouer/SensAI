import uuid
from dataclasses import dataclass, field

from core.conversation import (
    ConversationNotFoundError,
    IConversationService,
    MessageNotFoundError,
)
from core.messages import AIMessage, HumanMessage, IMessage, SystemMessage, ToolMessage


@dataclass
class InMemoryConversationData:
    messages: dict[str, IMessage] = field(default_factory=dict)
    parent_ids: dict[str, str | None] = field(default_factory=dict)
    active_message_id: str | None = None
    user_id: str | None = None


class InMemoryConversation(IConversationService):
    def __init__(self) -> None:
        self._conversations: dict[str, InMemoryConversationData] = {}

    def create_conversation(
        self,
        user_id: str,
        system_prompt: str | None = None,
    ) -> str:
        conversation_id: str = str(uuid.uuid4())
        self._conversations[conversation_id] = InMemoryConversationData(user_id=user_id)
        if system_prompt:
            self.add_system_message(
                conversation_id, SystemMessage(content=system_prompt)
            )
        return conversation_id

    """Getters"""

    def get_conversation_by_id_or_none(
        self, conversation_id: str
    ) -> InMemoryConversationData | None:
        return self._conversations.get(conversation_id)

    def get_message_by_id_or_none(
        self, conversation_id: str, message_id: str
    ) -> IMessage | None:
        conversation = self.get_conversation_by_id_or_none(conversation_id)
        if not conversation:
            return None
        return conversation.messages.get(message_id)

    def get_conversation_by_id(self, conversation_id: str) -> InMemoryConversationData:
        conversation = self.get_conversation_by_id_or_none(conversation_id)
        if not conversation:
            raise ConversationNotFoundError(conversation_id)
        return conversation

    def get_message_by_id(self, conversation_id: str, message_id: str) -> IMessage:
        self.get_conversation_by_id(conversation_id)
        message = self.get_message_by_id_or_none(conversation_id, message_id)
        if not message:
            raise MessageNotFoundError(message_id)
        return message

    def get_active_message(self, conversation_id: str) -> IMessage | None:
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation.active_message_id:
            return None
        return conversation.messages[conversation.active_message_id]

    def get_full_history(self, conversation_id: str) -> list[IMessage]:
        conversation = self.get_conversation_by_id(conversation_id)
        return list(conversation.messages.values())

    def get_used_history(self, conversation_id: str) -> list[IMessage]:
        conversation = self.get_conversation_by_id(conversation_id)

        history: list[IMessage] = []
        current_id = conversation.active_message_id
        while current_id:
            history.append(conversation.messages[current_id])
            current_id = conversation.parent_ids[current_id]
        history.reverse()
        return history

    """Small generics function to handle data."""

    def _store_message(
        self,
        conversation: InMemoryConversationData,
        message: IMessage,
        parent_id: str | None,
    ) -> IMessage:
        if message.id in conversation.messages:
            raise ValueError(f"Message '{message.id}' already exists")

        conversation.messages[message.id] = message
        conversation.parent_ids[message.id] = parent_id
        conversation.active_message_id = message.id
        return message

    """Business Logic"""

    def add_message(self, conversation_id: str, message: IMessage) -> IMessage:
        conversation = self.get_conversation_by_id(conversation_id)
        return self._store_message(
            conversation, message, parent_id=conversation.active_message_id
        )

    def edit_message(
        self, conversation_id: str, message_id: str, message: IMessage
    ) -> IMessage:
        conversation = self.get_conversation_by_id(conversation_id)
        if message_id not in conversation.messages:
            raise MessageNotFoundError(message_id)

        return self._store_message(
            conversation, message, parent_id=conversation.parent_ids[message_id]
        )

    def add_ai_message(self, conversation_id: str, message: AIMessage) -> IMessage:
        return self.add_message(conversation_id, message)

    def add_tool_message(self, conversation_id: str, message: ToolMessage) -> IMessage:
        return self.add_message(conversation_id, message)

    def add_human_message(
        self, conversation_id: str, message: HumanMessage
    ) -> IMessage:
        return self.add_message(conversation_id, message)

    def add_system_message(
        self, conversation_id: str, message: SystemMessage
    ) -> IMessage:
        return self.add_message(conversation_id, message)

    def clear(self, conversation_id: str) -> None:
        self.get_conversation_by_id(conversation_id)
        del self._conversations[conversation_id]
